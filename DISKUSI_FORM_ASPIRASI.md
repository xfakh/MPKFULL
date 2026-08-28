# Diskusi Pengembangan Form Aspirasi Internal MPK

**Tanggal:** 27 Agustus 2026

## Latar Belakang
Website MPK sudah memiliki tampilan yang memuaskan. Namun, saran dari guru adalah agar siswa tidak perlu berpindah ke Google Docs/Google Forms eksternal. Form aspirasi harus tetap berada di halaman website.

## Requirement Form Aspirasi

### Field yang Diperlukan:
- ✅ Nama lengkap (wajib)
- ✅ Kelas: 10A, 10B, 10C, 10D, 10E, 11A, 11B, 11C, 11D, 11E, 12A, 12B, 12C, 12D, 12E (wajib)
- ✅ Gender: Putra/Putri (wajib)
- ✅ Kategori aspirasi: Akademik, Non-akademik, Fasilitas, Lainnya (wajib)
- ✅ Deskripsi aspirasi (wajib)

### Fitur:
- ✅ Gender selection interaktif dengan gambar (Putra/Putri)
- ✅ Validasi semua field wajib diisi
- ✅ Loading animation saat submit
- ✅ Success modal dengan konfirmasi
- ✅ Design konsisten dengan website (Tailwind CSS + custom colors MPK)

## Status Implementasi

### ✅ SELESAI: Form Aspirasi Internal
**File:** `krisisan.html`

**Yang sudah diimplementasi:**
- Form aspirasi internal (tidak redirect ke Google Forms)
- Gender selection interaktif
- Semua field required dengan validasi
- UI/UX responsive dan konsisten dengan theme website
- Loading modal saat submit
- Success modal dengan opsi kembali ke beranda
- Reset form functionality

**Sistem Penyimpanan Saat Ini:**
- Data disimpan ke `localStorage` browser
- Temporary solution (data hanya di browser penggnya)
- Key: `mpk_last_aspirasi`
- Format JSON dengan timestamp

## Diskusi: Penyimpanan Data Aspirasi

### Opsi yang Dibahas:

#### 1. **Google Sheets** (dengan Apps Script)
- ✅ Gratis
- ✅ Mudah kelola (non-teknis)
- ✅ Export ke Excel
- ❌ Bergantung layanan eksternal

#### 2. **Firebase** (Google)
- ✅ Gratis tier cukup
- ✅ Realtime database
- ❌ Bergantung layanan eksternal

#### 3. **Backend Custom (PHP/Node.js/Bun) + SQLite**
- ✅ Kontrol penuh
- ✅ Data aman di server sendiri
- ❌ Perlu setup backend
- ✅ **PILIHAN TERBAIK untuk solusi mandiri**

#### 4. **PHP + SQLite**
- ✅ Umum tersedia di shared hosting
- ✅ SQLite file-based (tidak perlu MySQL server)
- ✅ Mudah backup
- ⚠️ Perlu PHP server

#### 5. **Bun + SQLite** (REKOMENDASI)
- ✅ Minimal setup (20-30 baris code)
- ✅ Integrated SQLite support
- ✅ Modern, cepat
- ✅ 1 file server saja
- ⚠️ Node.js ecosystem baru

### Keputusan:
**User memilih: SQLite sebagai database**

Saat ini: **localStorage** (temporary, data hanya di browser)

Saat mau implement backend:
- Buat endpoint API (PHP atau Bun)
- Ubah bagian `console.log()` menjadi `fetch()` ke backend
- Backend save ke SQLite

## Implementation Plan (Pending)

### Fase 1: ✅ DONE
- [x] Buat form aspirasi internal HTML
- [x] Gender selection interaktif
- [x] Validasi form
- [x] UI/UX responsive
- [x] Success modal

### Fase 2: PENDING (Saat akan dilakukan)
- [ ] Setup Bun/PHP server
- [ ] Setup SQLite database
- [ ] Buat endpoint untuk save aspirasi
- [ ] Buat endpoint untuk get/view aspirasi
- [ ] Dashboard admin untuk lihat aspirasi
- [ ] Export aspirasi ke CSV/Excel

## Catatan Teknis

### Struktur File Saat Ini:
```
MPKFULL/
├── index.html (halaman utama)
├── krisisan.html (form aspirasi - NEW)
├── krisismpk.css (styling)
└── assets/
    ├── mpkphotos.jpeg
    ├── gambar-putra.png
    └── gambar-putri2.png
```

### Teknologi yang Digunakan:
- HTML5
- Tailwind CSS (via CDN)
- Font Awesome (icons)
- Vanilla JavaScript (ES6+)
- localStorage API (temporary)

### Design System:
- Primary Color: `#0f6b4f` (emerald green)
- Accent: `#ffd166` (yellow)
- Responsive: mobile-first design
- Animations: Tailwind + custom CSS

## Next Steps (Dikerjakan Saat Diperlukan)

1. **Implementasi Backend:**
   - Pilih antara Bun atau PHP
   - Setup SQLite database
   - Buat API endpoint `/api/aspirasi/save`

2. **Dashboard Admin:**
   - View semua aspirasi yang masuk
   - Filter by kategori, kelas, gender
   - Export ke CSV

3. **Notifikasi:**
   - Email notification saat aspirasi masuk
   - Reminder ke guru/MPK

---
**Status:** Form aspirasi internal selesai dan berfungsi. Menunggu keputusan untuk implementasi backend SQLite.
