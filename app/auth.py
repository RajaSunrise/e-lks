"""Login admin (guru): nama pengguna + kata sandi + sesi."""
import hashlib
import hmac
import os

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "guru123")  # WAJIB diganti di server asli!
REKAP_KEY = os.getenv("REKAP_KEY", "")
SECRET = os.getenv("SECRET_KEY", "ganti-kalimat-rahasia-ini")


def _hash(teks):
    return hashlib.sha256(str(teks).encode()).hexdigest()


def cek_masuk(pengguna, sandi):
    return (hmac.compare_digest(str(pengguna), ADMIN_USER)
            and hmac.compare_digest(_hash(sandi), _hash(ADMIN_PASS)))


def sudah_masuk(req):
    return bool(req.session.get("admin"))


def boleh_rekap(req, kunci=""):
    return sudah_masuk(req) or (REKAP_KEY and kunci == REKAP_KEY)
