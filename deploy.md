# Deploy dengan Vercel

Panduan ini untuk guru/teknisi. Ada 2 pilihan — **Pilihan A disarankan** (paling sederhana).

## Penting dipahami dulu

- **Vercel hanya bisa menampung halaman depannya** (tampilan E-LKS).
- **Server FastAPI + file SQLite harus tetap jalan di server** (komputer sekolah/VPS), karena Vercel menghapus file setiap selesai request sehingga nilai akan hilang bila disimpan di sana.
- Kabar baiknya: kode sudah disiapkan agar keduanya tersambung otomatis.

## Pilihan A (disarankan): semua di 1 server

Tidak perlu Vercel sama sekali.

1. Salin seluruh folder proyek ke server/komputer sekolah.
2. `cd backend` → `pip install -r requirements.txt` → `uvicorn main:app --host 0.0.0.0 --port 8000`
3. Siswa buka `http://alamat-server:8000`, guru buka `http://alamat-server:8000/admin`.
4. Selesai — nilai otomatis masuk ke `backend/data/rekap.sqlite`.

## Pilihan B: fullstack di Vercel (halaman + server jadi satu)

1. **Naikkan kode ke GitHub** (termasuk folder ini, `api/`, `vercel.json`, `requirements.txt`).
2. Buka **vercel.com** → Add New → Project → Import repositori ini → Deploy. Tidak perlu diatur apa-apa — halaman utama, halaman E-LKS, `/admin`, dan API langsung tampil (tidak not-found lagi).
3. **Uji:** buka alamat Vercel → kerjakan 1 E-LKS sampai Hitung Nilai → buka `alamat/admin` → masuk → nilai harus tampil.
4. Biarkan `window.ELKS_API_BASE = "";` (kosong) di `index.html` — depan dan server sudah satu alamat.

**Penting:** di Vercel, file database bersifat **sementara** (hilang saat deploy ulang / server tidur). Untuk arsip permanen penelitian: unduh CSV/Bank Data berkala dari `/admin` ke folder `bank-data/`, atau pakai Pilihan A untuk data permanen.

## Cek bila gagal

- Masih not-found setelah deploy: pastikan file `vercel.json`, `api/index.py`, dan `requirements.txt` ikut ter-upload → Redeploy di dashboard Vercel.
- Not-found di server sendiri: pastikan perintah dijalankan **dari dalam folder `backend/`** (`cd backend` dulu) dan file `index.html` ada di folder proyek sejajar `backend/`. Bila tetap hilang, halaman utama kini menampilkan pesan penyebabnya, bukan not-found kosong.
- Status “Gagal terkirim, periksa internet” (Pilihan B lama dengan server terpisah): alamat server salah / server mati / HP tidak se-jaringan (pakai WiFi yang sama bila server lokal).
- Halaman admin (`/admin`) selalu dibuka dari **alamat yang sama dengan webnya**.

## Catatan arsip

Salin file `backend/data/rekap.sqlite` berkala (mis. per kelas) ke folder `bank-data/` sebagai arsip penelitian.
