"""E-LKS Backend (FastAPI): halaman + API nilai + login admin + rekap & cetak.

Jalankan dari folder proyek:  uvicorn app.main:app --host 0.0.0.0 --port 8000
Atur lewat environment: ADMIN_USER, ADMIN_PASS, REKAP_KEY, SECRET_KEY
"""
import io
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .auth import REKAP_KEY, SECRET, boleh_rekap, cek_masuk
from .database import DATA_DIR, DB_PATH, KOLOM, init_db, konek

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
STATIK = ROOT / "static"

init_db()

print("E-LKS Backend jalan.")
print("Folder halaman :", TEMPLATES, ("(index.html ADA)" if (TEMPLATES / "index.html").is_file() else "(index.html TAK ADA!)"))
print("File database  :", DB_PATH)

app = FastAPI(title="E-LKS Backend", docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key=SECRET)
# Izin akses dari depan yang di-hosting terpisah. Kirim nilai tak butuh cookie.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/api/kirim")
async def kirim(req: Request):
    try:
        d = await req.json()
    except Exception:
        return JSONResponse({"ok": False}, status_code=400)
    if not isinstance(d, dict) or not d.get("nama") or d.get("total") is None:
        return JSONResponse({"ok": False}, status_code=400)
    with konek() as c:
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
    if cek_masuk(d.get("pengguna", ""), d.get("sandi", "")):
        req.session["admin"] = True
        return {"ok": True}
    return JSONResponse({"ok": False}, status_code=401)


@app.post("/api/logout")
async def logout(req: Request):
    req.session.clear()
    return {"ok": True}


@app.get("/api/rekap")
async def rekap(req: Request, kunci: str = "", format: str = ""):
    if not boleh_rekap(req, kunci):
        return JSONResponse({"ok": False}, status_code=401)
    with konek() as c:
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
    return FileResponse(TEMPLATES / "admin.html")


@app.get("/", include_in_schema=False)
async def akar():
    """Halaman utama = halaman E-LKS (materi). Rute eksplisit agar tak pernah not-found."""
    idx = TEMPLATES / "index.html"
    if idx.is_file():
        return FileResponse(idx)
    return PlainTextResponse(
        "File halaman depan (index.html) tidak ditemukan.\n"
        f"Folder yang diperiksa: {TEMPLATES}\n"
        "Pastikan susunannya seperti ini:\n"
        "  budi-biologi/  <- folder proyek\n"
        "    templates/index.html, static/, app/, api/\n"
        "Lalu jalankan dari folder proyek:  uvicorn app.main:app --host 0.0.0.0 --port 8000",
        status_code=404,
    )


# File tampilan (css/js/gambar) disajikan terakhir agar /api/* tetap menang.
app.mount("/", StaticFiles(directory=str(STATIK), html=False), name="statik")
