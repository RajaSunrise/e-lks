# Backend E-LKS (FastAPI + file SQLite + login admin)

## Menjalankan di laptop/komputer sekolah
1. Masuk folder ini: `cd backend`
2. Pasang kebutuhan sekali saja: `pip install -r requirements.txt`
3. Jalankan: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Buka di peramban: siswa → `http://localhost:8000` (atau alamat komputer, mis. `http://192.168.1.10:8000`), guru → `http://localhost:8000/admin`

Login bawaan: pengguna `admin`, kata sandi `guru123` — **wajib diganti** lewat environment (`ADMIN_USER`, `ADMIN_PASS`) di komputer/server asli.

## Data
Tersimpan otomatis di file **`backend/data/rekap.sqlite`** (1 file, bisa disalin sebagai arsip per kelas).

## Alamat penting (otomatis)
- `POST /api/kirim` — menerima nilai dari halaman E-LKS (dipakai otomatis, tanpa diatur).
- `GET /api/rekap` — rekap JSON (khusus admin masuk / kunci `REKAP_KEY`).
- `GET /api/rekap?format=csv` — unduh rekap Excel.
- `GET /admin` — halaman admin: masuk → rekap + saring + rata-rata + cetak/PDF + unduh + keluar.

## Menayangkan di server/internet
Salin seluruh folder proyek ke server, atur 4 environment (`ADMIN_USER`, `ADMIN_PASS`, `REKAP_KEY`, `SECRET_KEY`), lalu jalankan dari folder `backend/`: `uvicorn main:app --host 0.0.0.0 --port 8000` (port menyesuaikan server). Tidak perlu layanan database lain — cukup FastAPI ini. Catatan: bila server menghapus file saat restart, salin `rekap.sqlite` berkala sebagai arsip.
