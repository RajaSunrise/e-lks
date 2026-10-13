# api/index.py — pintu masuk agar FastAPI tampil di Vercel.
# Vercel meneruskan SEMUA alamat ke sini (lihat vercel.json),
# lalu FastAPI menyajikan halaman statis + API + halaman admin.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app  # noqa: E402

try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:  # fallback saat uji lokal tanpa mangum
    handler = None
