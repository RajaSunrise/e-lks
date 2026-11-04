# E-LKS 1–4 Keanekaragaman Hayati Berbasis PBL (MAN Lombok Barat)

Lembar Kerja Siswa elektronik **per pertemuan (E-LKS 1–4)** untuk belajar dengan **model Problem Based Learning** sekaligus melatih **berpikir kritis** (Biologi Kelas X).

## Isi website (17 halaman)
Beranda (4 kartu E-LKS bergambar) → Identitas → Rancangan → E-LKS 1 (materi & tugas) → E-LKS 2 (materi & tugas) → E-LKS 3 (materi & tugas) → E-LKS 4 (materi & tugas) → Kuis → Isian & Uraian → Hasil → **Galeri (18 gambar contoh)** → Halaman Guru → Glosarium.

Rancangan tiap E-LKS (masalah + pertanyaan pemandu) ada di halaman **Rancangan** website, disusun berdasarkan **Indikator Kemampuan Berpikir Kritis (Ennis)** serta **Sintaks Problem Based Learning (PBL) dan Peran e-LKS**.

### Indikator Kemampuan Berpikir Kritis (Ennis)
1. **Memberikan penjelasan sederhana**: Memfokuskan pertanyaan; menganalisis argumen; bertanya dan menjawab pertanyaan klarifikasi
2. **Membangun keterampilan dasar**: Mempertimbangkan kredibilitas suatu sumber; mengobservasi dan mempertimbangkan hasil observasi
3. **Menyimpulkan**: Membuat deduksi dan mempertimbangkan hasil deduksi; membuat induksi dan mempertimbangkan hasil induksi; membuat dan mempertimbangkan nilai keputusan
4. **Memberikan penjelasan lanjut**: Mendefinisikan istilah dan mempertimbangkan suatu definisi; mengidentifikasi asumsi
5. **Mengatur strategi dan taktik**: Menentukan suatu tindakan; berinteraksi dengan orang lain

### Sintaks PBL dan Peran e-LKS
- **Fase 1: Orientasi peserta didik pada masalah**: Guru menjelaskan tujuan pembelajaran dan menyajikan masalah kontekstual; peserta didik memfokuskan permasalahan. *Peran e-LKS: e-LKS menyajikan wacana, gambar, atau video permasalahan.*
- **Fase 2: Mengorganisasikan peserta didik untuk belajar**: Guru membentuk kelompok dan membantu peserta didik merumuskan pertanyaan serta membagi tugas. *Peran e-LKS: e-LKS memuat petunjuk dan ruang perumusan masalah.*
- **Fase 3: Membimbing penyelidikan kelompok**: Peserta didik mengumpulkan informasi, mengobservasi, dan mencari penjelasan; guru membimbing. *Peran e-LKS: e-LKS memuat tautan sumber belajar dan pertanyaan pemandu berpikir kritis.*
- **Fase 4: Mengembangkan dan menyajikan hasil karya**: Kelompok menyusun dan mempresentasikan hasil; kelompok lain menanggapi. *Peran e-LKS: e-LKS memuat kolom jawaban dan hasil karya kelompok.*
- **Fase 5: Menganalisis dan mengevaluasi proses pemecahan masalah**: Guru dan peserta didik mengevaluasi proses dan hasil, lalu menarik kesimpulan. *Peran e-LKS: e-LKS memuat kesimpulan dan refleksi kelompok.*

Setiap pertemuan diawali **🎯 Tujuan Pembelajaran yang berorientasi berpikir kritis** — tampil di bawah judul tiap halaman materi E-LKS 1–4 dan diringkas di kartu beranda. Kegiatan 1 E-LKS 1 mirip **LKPD cetak pada contoh gambar**: identifikasi tingkat kehati 3 gambar + alasan, pilihan manfaat 4 contoh + contoh lain, lalu diskusi & kesimpulan (skor otomatis 10).

## Untuk siswa
1. Isi nama & kelas, ikuti tahap berurutan.
2. Jawaban **tersimpan otomatis** di perangkat — aman pindah halaman.
3. Di halaman Hasil, klik **Hitung Nilai & Simpan**, lalu cetak atau unduh laporan/Rekap Nilai (bisa dibuka di Excel).
4. Tombol **Bank Data (untuk Guru)** hanya dipakai bila diminta guru.

## Backend server sendiri (FastAPI + file SQLite + login admin) — disarankan

Struktur: `app/` (server: `main.py`, `database.py`, `auth.py`), `api/` (pintu Vercel), `static/` (tampilan), `templates/` (halaman).

1. `pip install -r requirements.txt` → `uvicorn app.main:app --host 0.0.0.0 --port 8000` (dari folder proyek)
2. Siswa buka `http://alamat-komputer:8000`, guru buka `http://alamat-komputer:8000/admin` (masuk: `admin` / `guru123` — wajib diganti lewat `ADMIN_USER`/`ADMIN_PASS`).
3. Data tersimpan di **1 file `data/rekap.sqlite`** — salin sebagai arsip per kelas.

Mau tayang di internet (Vercel)? Ikuti `deploy.md` — Vercel otomatis mendeteksi `app/main.py` sehingga semuanya tampil.

Bila web dibuka lewat server ini, nilai otomatis terkirim ke sana (tanpa mengatur tabel guru). Detail: `deploy.md`.

## Agar nilai SEMUA siswa terkumpul bila TETAP di GitHub Pages (wajib diatur guru 1x)

GitHub hanya menyimpan halaman web, sehingga nilai tiap siswa tersimpan di HP-nya masing-masing. Agar semuanya terkumpul otomatis di satu tabel milik guru:

1. Buka **sheets.google.com** → buat tabel “Rekap E-LKS” → tulis judul kolom di baris 1: `Waktu | Nama | Kelas | Absen | Madrasah | Tanggal | E-LKS1 | E-LKS2 | E-LKS3 | E-LKS4 | PG | Isian | Uraian | Total | Predikat | Interpretasi | Analisis | Evaluasi | Inferensi | Eksplanasi | Durasi`
2. Menu **Ekstensi → Apps Script** → hapus isi → tempel kode ini → Simpan:
```
function doPost(e) {
  var s = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var d = JSON.parse(e.postData.contents);
  s.appendRow([new Date(), d.nama, d.kelas, d.absen, d.sekolah, d.tanggal,
    d.e1, d.e2, d.e3, d.e4, d.pg, d.isian, d.uraian, d.total, d.predikat,
    d.interpretasi, d.analisis, d.evaluasi, d.inferensi, d.eksplanasi, d.durasi]);
  return ContentService.createTextOutput("OK");
}
```
3. **Terapkan (Deploy) → Aplikasi web** → akses “Siapa saja” → salin alamat web.
4. Buka website → Halaman Guru → tempel alamat di “Alamat rekap” → Simpan → Tes Kirim.

Siswa tidak perlu mengatur apa pun. Tiap siswa yang menekan “Hitung Nilai & Simpan” otomatis masuk sebagai baris baru (perlu internet; jika luring, terkirim otomatis di pengerjaan berikutnya).

## Cara kerja rekap otomatis (fullstack FastAPI - tanpa layanan lain)

Satu-satunya backend adalah folder `app/` (FastAPI + file SQLite). Bila web dibuka lewat server itu, tiap “Hitung Nilai & Simpan” otomatis masuk ke `data/rekap.sqlite` — tanpa layanan lain apa pun. Bila dibuka di GitHub Pages (tanpa server), website otomatis memakai cara tabel guru di bawah. Menyalakan server cukup sekali (lihat “Backend server sendiri” di atas).

## Untuk guru/peneliti
- Bobot: E-LKS 1–4 masing-masing 10, Kuis 40, Isian 10, Uraian 10 (total 100, KKM 75).
- Profil 5 aspek berpikir kritis (interpretasi, analisis, evaluasi, inferensi, eksplanasi) muncul otomatis di Hasil dan ikut terunduh di Rekap Nilai.
- Panduan urutan pertemuan (pretest → treatment → posttest) ada di halaman **Rancangan**.
- Kunci jawaban ada di halaman **Halaman Guru**.
- Simpan file **Bank Data** tiap kelas ke folder `bank-data`, contoh laporan ke folder `hasil`.

## Ganti foto
Taruh foto asli ke folder `assets/images` dengan nama yang sama persis (daftar nama ada di folder itu). Selama belum diganti, website memakai foto contoh dari internet.

## Menayangkan website (bagian teknisi)
Unggah semua file ke GitHub, lalu aktifkan Pages: **Settings → Pages → Deploy from branch → `main` / root**. Alamatnya menjadi `https://username.github.io/nama-repo/`.
