# Dokumentasi Integrasi Admin Organisasi ke Admin MPK

## Ringkasan Perubahan

Fitur admin organisasi telah berhasil digabungkan ke dalam dashboard admin MPK (`dashboard.html`). Admin MPK sekarang memiliki kontrol penuh atas organisasi sekolah dan file-file yang diupload.

---

## File yang Dimodifikasi

### 1. `templates/dashboard.html`

#### Perubahan HTML:
- **Sidebar**: Menambahkan menu baru:
  - "Manajemen Organisasi" → toggle menu untuk organisasi
  - "File Organisasi" → toggle menu untuk file organisasi
- **Organizations Section**: Tabel untuk menampilkan daftar organisasi
- **Files Section**: Tabel untuk menampilkan file organisasi dengan filter
- **Modal Add Org**: Form untuk menambah organisasi baru

#### Perubahan JavaScript:
```javascript
// Fungsi navigasi sidebar
function showOrganizations() - tampilkan section organisasi
function showFiles() - tampilkan section file organisasi

// Fungsi organisasi
function loadOrganizations() - ambil data dari API
function renderOrganizations() - render tabel
function showAddOrgModal() - tampilkan modal
function closeAddOrgModal() - sembunyikan modal
function deleteOrganization(id, name) - hapus organisasi

// Fungsi file
function loadFiles() - ambil data file (dengan filter)
function renderFiles() - render tabel file
function updateOrgFilter() - update dropdown filter
```

---

### 2. `app.py`

#### Rute API yang Ditambahkan/Diperbarui:

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/organizations` | GET | Daftar semua organisasi (dengan jumlah file) |
| `/api/organizations` | POST | Tambah organisasi baru |
| `/api/organizations/<id>` | DELETE | Hapus organisasi |
| `/api/org/admin/organizations` | GET | Daftar file organisasi (admin) |
| `/api/org/admin/download/<file_id>` | GET | Download file organisasi |
| `/api/organizations/<id>/toggle-status` | PUT | Toggle status aktif/nonaktif |
| `/api/org/admin/files/<file_id>/status` | PUT | Update status file (verifikasi) |
| `/api/org/admin/files/<file_id>` | DELETE | Hapus file organisasi |

#### Route yang Dihapus:
- `/org/admin/dashboard` → Digabung ke `/dashboard`
- `org_admin_dashboard()` → Tidak diperlukan lagi

---

## Fitur yang Tersedia di Admin MPK

### 1. Manajemen Organisasi

#### Menambah Organisasi Baru
- Klik "Manajemen Organisasi" di sidebar
- Klik "Tambah Organisasi"
- Isi form: Nama, Username, Email, Password
- Klik "Simpan"

#### Melihat Daftar Organisasi
- Tampilkan dengan format:
  - Nama organisasi (dengan ikon)
  - Username (login)
  - Email
  - Jumlah file yang diupload
  - Status (Aktif/Nonaktif)

#### Menghapus Organisasi
- Klik ikon trash pada baris organisasi
- Konfirmasi penghapusan (akan menghapus semua file terkait)

#### Toggle Status Organisasi
- Ubah status antara Aktif/Nonaktif
- Mempengaruhi akses login organisasi

### 2. File Organisasi

#### Melihat File
- Klik "File Organisasi" di sidebar
- Lihat semua file atau filter berdasarkan organisasi
- Tampilkan dengan format:
  - Nama organisasi
  - Nama file
  - Tipe file (extensi)
  - Ukuran file (KB)
  - Waktu upload
  - Tombol download

#### Download File
- Klik ikon download pada baris file
- File akan di-download dari server

#### Verifikasi/Update Status File
- Status file: uploaded/diproses/selesai
- Admin bisa mengubah status untuk tracking

#### Hapus File
- Klik tombol delete pada baris file
- Konfirmasi penghapusan

---

## Struktur Data

### Tabel Organizations

| Field | Type | Deskripsi |
|-------|------|-----------|
| id | Integer | Primary key |
| name | String | Nama organisasi (tampilan) |
| username | String | Username login |
| email | String | Email organisasi |
| password | String | Hash password |
| status | String | active/nonactive |
| created_at | DateTime | Waktu pembuatan |

### Tabel OrganizationFile

| Field | Type | Deskripsi |
|-------|------|-----------|
| id | Integer | Primary key |
| organization_id | Integer | Foreign key ke organizations |
| file_name | String | Nama file asli |
| file_type | String | Extensi file |
| file_size | Integer | Ukuran dalam bytes |
| file_path | String | Lokasi file di server |
| description | Text | Deskripsi file |
| status | String | uploaded/diproses/selesai |
| uploaded_at | DateTime | Waktu upload |

---

## Cara Menggunakan

### 1. Install Dependencies (jika belum)
```bash
pip3 install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python3 app.py
```

### 3. Akses Admin Dashboard
1. Buka browser ke `http://localhost:5000`
2. Login sebagai admin:
   - Username: `admin`
   - Password: `mpkassalafiyyah`
3. Setelah login, akan diarahkan ke dashboard
4. Klik menu di sidebar:
   - "Manajemen Organisasi" untuk kelola akun organisasi
   - "File Organisasi" untuk melihat dan mengelola file

---

## Testing Checklist

### Manajemen Organisasi
- [ ] Tambah organisasi baru
- [ ] Lihat daftar organisasi
- [ ] Hapus organisasi
- [ ] Toggle status organisasi
- [ ] Validasi data (email, username unique)
- [ ] Filter organisasi di menu file

### File Organisasi
- [ ] Lihat semua file
- [ ] Filter berdasarkan organisasi
- [ ] Download file
- [ ] Update status file
- [ ] Hapus file
- [ ] Validasi jumlah file per organisasi

### Integrasi
- [ ] Menu navigasi berfungsi
- [ ] Toast notification muncul untuk feedback
- [ ] Loading state saat ambil data
- [ ] Empty state saat belum ada data
- [ ] Modal đóng/buka dengan benar
- [ ] Form submission berhasil

---

## Troubleshooting

### Error: "Akses ditolak. Hanya admin yang dapat melakukan ini."
- Pastikan login sebagai admin, bukan organisasi
- Cek session browser

### Error: "Data tidak ditemukan"
- Pastikan database sudah di-migrate: `flask db upgrade`
- Cek data di database: `sqlite3 data/aspirasi.db`

### File tidak muncul di menu File Organisasi
- Pastikan organisasi sudah mengupload file
- Cek folder `data/uploads/organization/`
- Klik tombol "Refresh" di header tabel

### Form tambah organisasi tidak submit
- Pastikan all field diisi (nama, username, email, password)
- Cek console browser untuk error JavaScript
- Validasi format email (harus valid email format)

---

## Catatan Keamanan

- Password organisasi di-hash menggunakan PBKDF2-SHA256
- Route menggunakan decorator `@admin_required`
- File upload harus melalui validasi tipe file
- Sanitasi input untuk mencegah XSS
- Konfirmasi sebelum penghapusan data (menghapus organisasi juga menghapus file terkait)

---

## Dokumentasi Terkait

- `ANALISIS_STATUS_LENGKAP.md` - Analisis status sistem
- `BUGFIX_REPORT.md` - Laporan bugfix
- `DOKUMENTASI_SISTEM_ORGANISASI.md` - Dokumentasi asli sistem organisasi
- `TESTING_GUIDE.md` - Panduan testing lengkap

---

*Dokumen ini dibuat pada: 2026-09-24*
