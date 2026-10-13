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

## Pilihan B: halaman depan di Vercel + server di sekolah

1. **Naikkan kode ke GitHub** (termasuk folder ini).
2. Buka **vercel.com** → Add New → Project → Import repositori ini → Deploy. Tidak perlu diatur apa-apa (halaman depan tayang otomatis).
3. **Nyalakan server** di komputer sekolah seperti Pilihan A langkah 2. Catat alamatnya, mis. `http://192.168.1.10:8000` (atau alamat internet bila server online).
4. **Sambungkan:** di file `index.html`, cari baris ini lalu isi alamat server:
```
<script>window.ELKS_API_BASE = "";</script>
```
menjadi (contoh):
```
<script>window.ELKS_API_BASE = "http://192.168.1.10:8000";</script>
```
5. Simpan → `git push` (Vercel menerbitkan ulang otomatis).
6. **Uji:** buka web Vercel → kerjakan 1 E-LKS sampai Hitung Nilai → cek `/admin` di server: nilai harus masuk.

## Cek bila gagal (Pilihan B)

- Status “Gagal terkirim, periksa internet”: alamat server salah / server mati / HP siswa tidak se-jaringan dengan server (pakai WiFi yang sama bila server lokal).
- Nilai masuk tapi rekap kosong: pastikan melihat rekap di **server** (`/admin`), bukan di Vercel.
- Halaman admin (`/admin`) selalu dibuka dari **alamat server**, bukan alamat Vercel.

## Catatan arsip

Salin file `backend/data/rekap.sqlite` berkala (mis. per kelas) ke folder `bank-data/` sebagai arsip penelitian.
