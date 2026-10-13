"""Backend E-LKS: FastAPI + file SQLite + login admin + rekap & cetak.

Jalankan:  uvicorn main:app --host 0.0.0.0 --port 8000   (dari folder backend/)
Atur lewat environment: ADMIN_USER, ADMIN_PASS, REKAP_KEY, SECRET_KEY
"""
import hashlib
import hmac
import io
import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

BASE = Path(__file__).resolve().parent
DEPAN = BASE.parent  # folder proyek (berisi index.html)
# Di Vercel, folder proyek hanya-baca sehingga database pindah ke /tmp.
DATA_DIR = Path("/tmp/elks-data") if os.getenv("VERCEL") else BASE / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "rekap.sqlite"

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "guru123")  # WAJIB diganti di server asli!
REKAP_KEY = os.getenv("REKAP_KEY", "")
SECRET = os.getenv("SECRET_KEY", "ganti-kalimat-rahasia-ini")

KOLOM = ["nama", "kelas", "absen", "sekolah", "tanggal", "e1", "e2", "e3", "e4",
         "pg", "isian", "uraian", "total", "predikat",
         "interpretasi", "analisis", "evaluasi", "inferensi", "eksplanasi", "durasi"]


def _hash(teks):
    return hashlib.sha256(str(teks).encode()).hexdigest()


def _db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def _init():
    with _db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS rekap (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT, kelas TEXT, absen TEXT, sekolah TEXT, tanggal TEXT,
            e1 REAL, e2 REAL, e3 REAL, e4 REAL, pg REAL, isian REAL, uraian REAL,
            total REAL, predikat TEXT,
            interpretasi REAL, analisis REAL, evaluasi REAL, inferensi REAL, eksplanasi REAL,
            durasi TEXT, dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")


_init()

app = FastAPI(title="E-LKS Backend", docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key=SECRET)
# Izin akses dari depan yang di-hosting terpisah (mis. Vercel). Kirim nilai tak butuh cookie.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


def _admin(req: Request):
    return bool(req.session.get("admin"))


@app.post("/api/kirim")
async def kirim(req: Request):
    try:
        d = await req.json()
    except Exception:
        return JSONResponse({"ok": False}, status_code=400)
    if not isinstance(d, dict) or not d.get("nama") or d.get("total") is None:
        return JSONResponse({"ok": False}, status_code=400)
    with _db() as c:
        c.execute(
            f"INSERT INTO rekap ({','.join(KOLOM)}) VALUES ({','.join('?' * len(KOLOM))})",
            [d.get(k, "") for k in KOLOM],
        )
    return {"ok": True}


@app.post("/api/login")
async def login(req: Request):
    try:
        d = await req.json()
    except Exception:
        return JSONResponse({"ok": False}, status_code=400)
    if (hmac.compare_digest(str(d.get("pengguna", "")), ADMIN_USER)
            and hmac.compare_digest(_hash(d.get("sandi", "")), _hash(ADMIN_PASS))):
        req.session["admin"] = True
        return {"ok": True}
    return JSONResponse({"ok": False}, status_code=401)


@app.post("/api/logout")
async def logout(req: Request):
    req.session.clear()
    return {"ok": True}


@app.get("/api/rekap")
async def rekap(req: Request, kunci: str = "", format: str = ""):
    if not (_admin(req) or (REKAP_KEY and kunci == REKAP_KEY)):
        return JSONResponse({"ok": False}, status_code=401)
    with _db() as c:
        rows = [dict(r) for r in c.execute(
            "SELECT id,nama,kelas,absen,sekolah,tanggal,e1,e2,e3,e4,pg,isian,uraian,"
            "total,predikat,interpretasi,analisis,evaluasi,inferensi,eksplanasi,durasi,dibuat"
            " FROM rekap ORDER BY id DESC LIMIT 2000")]
    if format == "csv":
        buf = io.StringIO()
        kepala = (["id", "nama", "kelas", "absen", "sekolah", "tanggal", "e1", "e2", "e3", "e4",
                   "pg", "isian", "uraian", "total", "predikat",
                   "interpretasi", "analisis", "evaluasi", "inferensi", "eksplanasi", "durasi", "dibuat"])
        buf.write(",".join(kepala) + "\n")
        for r in rows:
            buf.write(",".join('"' + str(r.get(k, "")).replace('"', '""') + '"' for k in kepala) + "\n")
        return PlainTextResponse("\ufeff" + buf.getvalue(), media_type="text/csv; charset=utf-8",
                                 headers={"Content-Disposition": 'attachment; filename="rekap-elks.csv"'})
    return {"ok": True, "rows": rows}


@app.get("/admin")
async def halaman_admin():
    return FileResponse(BASE / "admin.html")


# Halaman depan (index.html dkk) disajikan terakhir agar /api/* tetap menang.
app.mount("/", StaticFiles(directory=str(DEPAN), html=True), name="depan")
