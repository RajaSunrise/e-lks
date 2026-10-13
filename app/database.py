"""Jalur database SQLite + pembuatan tabel rekap."""
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Di Vercel, folder proyek hanya-baca sehingga database pindah ke /tmp.
DATA_DIR = Path("/tmp/elks-data") if os.getenv("VERCEL") else ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "rekap.sqlite"

KOLOM = ["nama", "kelas", "absen", "sekolah", "tanggal", "e1", "e2", "e3", "e4",
         "pg", "isian", "uraian", "total", "predikat",
         "interpretasi", "analisis", "evaluasi", "inferensi", "eksplanasi", "durasi"]


def konek():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with konek() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS rekap (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT, kelas TEXT, absen TEXT, sekolah TEXT, tanggal TEXT,
            e1 REAL, e2 REAL, e3 REAL, e4 REAL, pg REAL, isian REAL, uraian REAL,
            total REAL, predikat TEXT,
            interpretasi REAL, analisis REAL, evaluasi REAL, inferensi REAL, eksplanasi REAL,
            durasi TEXT, dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
