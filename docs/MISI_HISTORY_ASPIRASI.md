# Misi: History / Feed Aspirasi Publik (Transparansi)

**Tanggal dicatat:** 7 November 2026
**Status:** Menunggu eksekusi (disetujui, sesuai default rekomendasi)
**Referensi desain:** https://ruvicode.com/realtime

---

## 1. Latar Belakang

Aplikasi sudah berjalan dengan baik dan siap dipakai menampung aspirasi siswa. Muncul permintaan tambahan: **siswa dapat melihat history aspirasi** yang masuk, sebagai bentuk transparansi MPK.

Inspirasi UI diambil dari feed `ruvicode.com/realtime`: daftar request mentah secara real-time, dengan stats cards di atas dan tabel lebar di bawahnya.

**Kolom yang diminta:** `Time`, `Kelas`, `Kategori`, `Deskripsi`, `Status`.
**Nama sengaja tidak ditampilkan** agar tetap anonim di antara siswa.

---

## 2. Keputusan yang Disepakati (Default)

| # | Item | Keputusan |
|---|------|-----------|
| 1 | Nama route | **`/transparansi`** (halaman publik, tanpa login) |
| 2 | Tema | **Light** (satu keluarga dengan situs existing, header tabel gelap) |
| 3 | Kode pelacak | **Ya**, tampilkan kode pendek (mis. `#A7F3`) agar siswa bisa mengenali aspirasinya |

Alternatif nama route yang dipertimbangkan: `/aspirasi-publik`, `/dinding-aspirasi`, `/feed-aspirasi`, `/realtime`.

---

## 3. Prinsip & Pertimbangan Anonimitas

Pemisahan halaman dari dashboard admin adalah keputusan sadar. Halaman publik **tidak** boleh mengirimkan data sensitif meski hanya disembunyikan di JS.

- **`nama` dan `gender` tidak pernah dikirim ke client.** Field dipotong di sisi server (bukan di-hide via JS), supaya tidak bisa dibaca lewat Network tab.
- **Risiko identifikasi implisit:** kombinasi `Kelas` + `Kategori` + `Waktu` bisa mengidentifikasi siswa di sekolah kecil, terlebih jika isi deskripsi menyebut nama guru/orang. Karena itu deskripsi ditampilkan ter-truncate dan bisa dimoderasi.
- **Babi liar / troll:** feed anonim yang dibaca semua siswa berpotensi memuat konten menjatuhkan siswa lain, bukan aspirasi. Perlu kesadaran moderasi (bisa jadi pengembangan lanjutan).

---

## 4. Ruang Lingkup Teknis

### 4.1 Backend — Endpoint Baru

`GET /api/aspirasi/public`

- **Publik**, tanpa autentikasi (tidak pakai `@login_required`).
- Field yang dikembalikan **hanya**: `id`, `code`, `created_at`, `kelas`, `kategori`, `deskripsi`, `status`.
- **Tidak pernah** mengembalikan `nama` dan `gender`.
- Query params:
  - `limit` (default `100`, dibatasi maksimum)
  - `status` (`pending` / `diproses` / `selesai`)
  - `kategori`
  - `kelas`
- Urutan: `created_at DESC`.
- `deskripsi` di-escape; pertimbangkan pemotongan panjang di server untuk list.

### 4.2 Backend — Kode Pendek

- Tambah kolom/derivasi **kode pendek** (mis. `#A7F3`) sebagai pelacak aspirasi.
- Opsi implementasi:
  - Kolom baru `code` di model `Aspirasi` (perlu migration), atau
  - Derivasi deterministik dari `id` (base36 / hash) tanpa migration.
- Kode dipilih karena lebih ramah dibaca siswa dibanding ID numerik.

### 4.3 Route & Template

- Route Flask: `@app.route('/transparansi')` → `render_template('transparansi.html')`.
- Template baru: `templates/transparansi.html`.
- Style: Tailwind via CDN + `krisismpk.css`, palette MPK (`#0f6b4f`, `#074a31`, `#ffd166`, Inter, Font Awesome).

---

## 5. Rancangan UI

Mengacu struktur referensi (dark, monospace time, tabel lebar, live indicator) namun disesuaikan ke identitas MPK.

### 5.1 Stats Cards (di atas tabel)

Meniru pola referensi, versi MPK:

1. **Total Aspirasi Masuk**
2. **Belum Diproses** (pending)
3. **Sedang Diproses** (diproses)
4. **Selesai** — diberi penekanan khusus (border hijau + persentase kecil di bawah angka).

Tujuan: siswa langsung melihat berapa persen aspirasi yang sudah selesai → panen transparansi.

### 5.2 Tabel

- **Sticky header** seperti referensi.
- Kolom: `Time`, `Kelas`, `Kategori`, `Deskripsi`, `Status` (+ kolom kode pendek).
- **Time**: jam kecil di atas + tanggal di bawah (mis. `14:32` / `7 Nov 2026`), `font-mono tabular-nums`.
- **Status**: badge berwarna konsisten dengan dashboard admin.
  - `pending` → merah
  - `diproses` → kuning (`#ffd166`)
  - `selesai` → hijau
- **Kelas**: chip abu-abu monospace (mis. `10A`).
- **Kategori**: chip hijau.
- **Deskripsi**: `line-clamp` 2 baris; klik → modal detail (menjaga tinggi baris seragam).
- Aksen kiri tipis pada baris mengikuti status (bukan warna latar penuh).

### 5.3 Live Indicator & Refresh

- Titik hijau berdenyut + teks "Auto refresh dalam Xs".
- **Auto refresh 15 detik** (hemat; bukan 5s seperti referensi).
- Tombol refresh manual.
- **Hentikan polling saat tab tidak aktif** (`document.hidden`).

### 5.4 Tema

- **Light**, menyatu dengan situs existing.
- Nuansa "feed/live monitor" dihadirkan lewat **panel tabel dengan header gelap, isi terang** — bukan dark theme penuh.

### 5.5 Sentuhan MPK

- Di bawah tabel: kalimat kecil *"Feed ini anonim. Nama tidak pernah ditampilkan."*
- Tautan **"Sampaikan aspirasi"** → `/krisisan`, sehingga halaman ini sekaligus menjadi pintu masuk formulir.

---

## 6. Nilai Tambah (Opsi Lanjutan)

- **Kode pendek sebagai pelacak:** ditampilkan di tabel (mis. `#A7F3`); siswa yang menyimpan kode dapat memantau aspirasinya.
- **Filter publik:** status / kategori. Filter `kelas` sebaiknya dipertimbangkan matang karena bisa memperbesar risiko identifikasi implisit.

---

## 7. Rencana Eksekusi (Checklist)

- [ ] Buat endpoint `GET /api/aspirasi/public` (tanpa `nama` & `gender`, dengan filter + limit).
- [ ] Tambahkan kode pendek aspirasi (migration kolom `code` atau derivasi dari `id`).
- [ ] Buat route `/transparansi` + template `transparansi.html`.
- [ ] Implementasi stats cards (Total / Pending / Diproses / Selesai + %).
- [ ] Implementasi tabel sticky header (Time, Kelas, Kategori, Deskripsi, Status + kode).
- [ ] Modal detail deskripsi (line-clamp 2 baris di tabel).
- [ ] Auto refresh 15s + tombol manual + pause saat tab hidden.
- [ ] Tambahkan link masuk di navbar halaman utama (`index.html`) dan setelah submit di form aspirasi (`krisisan.html`).
- [ ] Verifikasi: pastikan `nama` & `gender` benar-benar tidak ada di response (cek Network tab).

---

## 8. File yang Akan Disentuh

| File | Perubahan |
|------|-----------|
| `app.py` | Route `/transparansi`, endpoint `/api/aspirasi/public`, kolom/derivasi kode |
| `templates/transparansi.html` | **Baru** — halaman feed publik |
| `templates/index.html` | Link menu ke `/transparansi` |
| `templates/krisisan.html` | Link ke `/transparansi` setelah submit |
| `migrations/versions/*` | Migration kolom `code` (jika memilih opsi kolom) |
| `static/krisismpk.css` | Tambahan style tabel feed (bila perlu) |

---

**Catatan:** Dokumen ini mencatat keputusan sesuai default rekomendasi. Belum ada perubahan kode yang dilakukan.
