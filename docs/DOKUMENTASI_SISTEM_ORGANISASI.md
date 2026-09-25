# DOKUMENTASI SISTEM ORGANISASI MPK

## 📋 RINGKASAN IMPLEMENTASI

Sistem manajemen organisasi telah berhasil diimplementasikan sebagai modul tambahan pada website MPK yang sudah ada. Sistem ini memungkinkan organisasi sekolah untuk login, upload file, dan memungkinkan admin MPK untuk memonitor semua file dari organisasi.

---

## 🏗️ ARSITEKTUR SISTEM

### Database Schema

#### Tabel: organization
```sql
- id (PRIMARY KEY)
- name (UNIQUE) - Nama organisasi (contoh: OSIS, Rohis, Pramuka)
- username (UNIQUE) - Username untuk login organisasi
- password - Password ter-hash
- email (UNIQUE) - Email organisasi
- status - Status aktif/nonaktif
- created_at - Waktu pembuatan
- updated_at - Waktu update terakhir
```

#### Tabel: organization_file
```sql
- id (PRIMARY KEY)
- organization_id (FOREIGN KEY) - Relasi ke organization
- file_name - Nama file asli yang diupload
- file_path - Nama file yang tersimpan di server (unique)
- file_type - Ekstension file (pdf, docx, xlsx, dll)
- file_size - Ukuran file dalam bytes
- description - Keterangan file (opsional)
- status - Status file
- uploaded_at - Waktu upload
- updated_at - Waktu update terakhir
```

### Folder Struktur
```
data/
└── uploads/
    └── organization/
        └── [file-file organisasi]
```

---

## 🔐 SISTEM AUTENTIKASI

### Dual Login System

**1. Admin Login (Existing)**
- Route: `/login`
- Username: admin
- Password: mpkassalafiyyah
- Akses: Dashboard aspirasi siswa + Dashboard monitoring organisasi

**2. Organization Login (Baru)**
- Route: `/org/login`
- Username: diatur oleh admin (contoh: osis, rohis, pramuka)
- Password: diatur oleh admin saat membuat organisasi
- Akses: Dashboard organisasi + Upload file

### Flask-Login Integration
Sistem menggunakan Flask-Login dengan custom `get_id()` untuk membedakan:
- Admin: `admin_{id}`
- Organization: `org_{id}`

---

## 📍 ROUTE & ENDPOINT

### Organization Routes

| Route | Method | Auth | Deskripsi |
|-------|--------|------|-----------|
| `/org/login` | GET/POST | ❌ | Login organisasi |
| `/org/logout` | GET | ✅ Org | Logout organisasi |
| `/org/dashboard` | GET | ✅ Org | Dashboard organisasi |
| `/org/admin/dashboard` | GET | ✅ Admin | Dashboard admin monitoring org |

### Organization API Endpoints

| Endpoint | Method | Auth | Deskripsi |
|----------|--------|------|-----------|
| `/api/organizations` | GET | ✅ Admin | Dapatkan daftar organisasi |
| `/api/organizations` | POST | ✅ Admin | Buat organisasi baru |
| `/api/organizations/<id>` | DELETE | ✅ Admin | Hapus organisasi |
| `/api/org/files` | GET | ✅ Org | Dapatkan file organisasi |
| `/api/org/upload` | POST | ✅ Org | Upload file |
| `/api/org/files/<id>` | DELETE | ✅ Org | Hapus file milik org |
| `/api/org/admin/organizations` | GET | ✅ Admin | Dapatkan semua file org |
| `/api/org/admin/download/<id>` | GET | ✅ Admin | Download file |

---

## 💼 WORKFLOW PENGGUNAAN

### Sebagai Admin MPK

**1. Membuat Organisasi**
```
1. Login ke /login dengan admin/mpkassalafiyyah
2. Akses Dashboard Admin > Organisasi
3. Klik "Tambah Organisasi"
4. Isi: Nama, Username, Email, Password
5. Klik Simpan
6. Organisasi siap login
```

**2. Monitoring File Organisasi**
```
1. Di dashboard admin, pilih tab "File Organisasi"
2. Lihat semua file dari semua organisasi
3. Filter berdasarkan organisasi
4. Download file jika diperlukan
```

### Sebagai Organisasi

**1. Login Organisasi**
```
1. Buka /org/login
2. Masukkan username dan password yang diberikan admin
3. Klik Login
```

**2. Upload File**
```
1. Di dashboard organisasi, klik "File Upload"
2. Pilih file (drag-drop atau klik untuk browse)
3. Tambahkan keterangan (opsional)
4. Klik "Upload File"
```

**3. Melihat Riwayat Upload**
```
1. Di tab "File Upload", lihat tabel "Riwayat Upload"
2. Lihat semua file yang pernah diupload
3. Hapus file jika diperlukan dengan klik tombol trash
```

---

## 🔒 KEAMANAN

### Implementasi Keamanan

**1. Password Hashing**
- Semua password di-hash menggunakan `pbkdf2:sha256`
- Tidak ada password yang disimpan dalam plaintext

**2. File Upload Validation**
```python
- Validasi ekstensi file (whitelist)
- Validasi ukuran file maksimal 16MB
- Secure filename generation
- Files disimpan dengan nama random (UUID)
```

**3. Authorization**
- Organisasi hanya bisa mengakses file miliknya sendiri
- Backend mengvalidasi `organization_id` dari session, bukan dari user input
- Admin hanya bisa upload/manage jika memiliki role 'admin'

**4. Endpoint Protection**
```python
@login_required          # Harus login
@organization_required   # Hanya organisasi
@admin_required         # Hanya admin
```

---

## 📊 ALLOWED FILE TYPES

Ekstensi file yang diizinkan:
- Dokumen: `pdf`, `doc`, `docx`, `xls`, `xlsx`, `txt`
- Gambar: `png`, `jpg`, `jpeg`

**Maksimal ukuran file: 16MB**

---

## 🗂️ STRUKTUR FOLDER UPLOADS

```
data/uploads/organization/
├── a1b2c3d4e5f6.pdf          (File OSIS)
├── b2c3d4e5f6g7.docx         (File Rohis)
├── c3d4e5f6g7h8.xlsx         (File Pramuka)
└── d4e5f6g7h8i9.png          (File PMR)
```

File disimpan dengan nama acak (UUID) untuk keamanan. Nama file asli disimpan di database.

---

## 🧪 TESTING

### Test Cases

#### 1. Admin Login & Dashboard
- [x] Admin bisa login dengan credential default
- [x] Admin bisa akses dashboard aspirasi
- [x] Admin bisa akses dashboard organisasi

#### 2. Membuat Organisasi
- [x] Admin bisa membuat organisasi baru
- [x] Validasi username tidak boleh duplikat
- [x] Validasi email tidak boleh duplikat
- [x] Organisasi muncul di daftar

#### 3. Organization Login
- [x] Organisasi bisa login dengan credential yang benar
- [x] Organisasi tidak bisa login dengan credential salah
- [x] Organisasi ter-redirect ke dashboard setelah login

#### 4. File Upload
- [x] Organisasi bisa upload file
- [x] Validasi file size (max 16MB)
- [x] Validasi file type
- [x] File tersimpan di folder uploads/organization
- [x] Metadata file tersimpan di database

#### 5. File Management
- [x] Organisasi hanya lihat file miliknya
- [x] Organisasi bisa hapus file miliknya
- [x] Admin bisa lihat semua file dari semua organisasi
- [x] Admin bisa download file

#### 6. Authorization & Security
- [x] Organisasi tidak bisa akses file organisasi lain
- [x] Organisasi tidak bisa akses dashboard admin
- [x] Non-login user tidak bisa upload file
- [x] Password ter-hash di database

#### 7. Fitur Aspirasi Tetap Berjalan
- [x] Form aspirasi masih bisa diakses
- [x] Submit aspirasi masih berfungsi
- [x] Dashboard aspirasi admin masih berfungsi
- [x] Data aspirasi tidak terganggu

---

## 📱 TAMPILAN & UX

### Login Organisasi (`/org/login`)
- Clean & modern interface
- Consistent dengan design system MPK
- Password visibility toggle
- Flash messages untuk error/success

### Dashboard Organisasi (`/org/dashboard`)
- Sidebar navigation
- Stats cards (Total File, Total Upload, Total Size)
- File list dengan riwayat terbaru
- Upload section dengan drag-drop support
- Table dengan semua file history

### Admin Dashboard Organization (`/org/admin/dashboard`)
- Manajemen organisasi (CRUD)
- Monitoring semua file
- Filter berdasarkan organisasi
- Download file functionality
- Modal untuk tambah organisasi

---

## 🚀 CARA MENJALANKAN

### Development

```bash
# Aktifkan virtual environment
source venv/bin/activate

# Jalankan aplikasi
python app.py

# Akses di browser
http://127.0.0.1:5000
```

### Production (Docker)

```bash
# Build dan run
docker compose up -d --build

# Akses di browser
http://localhost:8080
```

---

## 📝 CONTOH ORGANISASI YANG BISA DIBUAT

Admin bisa membuat organisasi dengan struktur:

```
Nama Organisasi: OSIS
Username: osis
Email: osis@example.com
Password: [diatur oleh admin]

Nama Organisasi: Rohis
Username: rohis
Email: rohis@example.com
Password: [diatur oleh admin]

Nama Organisasi: Pramuka
Username: pramuka
Email: pramuka@example.com
Password: [diatur oleh admin]

Dan seterusnya...
```

---

## 🔄 INTEGRASI DENGAN FITUR ASPIRASI

Sistem organisasi **TERPISAH SEPENUHNYA** dari sistem aspirasi siswa:

**Aspirasi Siswa:**
- Route: `/krisisan`
- API: `/api/aspirasi`
- Database: `aspirasi` table
- Login: Tidak perlu login
- Tidak terpengaruh oleh sistem organisasi

**Organisasi:**
- Route: `/org/login`, `/org/dashboard`
- API: `/api/organizations`, `/api/org/files`
- Database: `organization`, `organization_file` tables
- Login: Perlu login khusus organisasi
- Tidak mengganggu fitur aspirasi

---

## ⚠️ CATATAN PENTING

1. **Database Backup**: Pastikan backup database secara berkala
2. **Upload Folder**: Pastikan folder `data/uploads/organization` memiliki write permission
3. **File Retention**: Admin perlu mengatur kebijakan kapan file akan dihapus
4. **Password Change**: Organisasi tidak bisa ganti password sendiri (harus melalui admin)

---

## 📞 TROUBLESHOOTING

### Error: "File tidak boleh lebih besar dari 16MB"
- Ukuran file melebihi limit
- Kompres file atau split menjadi beberapa bagian

### Error: "Tipe file tidak diizinkan"
- File format tidak ada di whitelist
- Gunakan format: PDF, Word, Excel, Image, TXT

### Organization tidak muncul di dashboard
- Refresh halaman
- Pastikan sudah klik "Tambah Organisasi" dan Simpan
- Check browser console untuk error

### File tidak tersimpan
- Pastikan folder `data/uploads/organization` ada
- Pastikan folder memiliki permission write
- Pastikan disk space cukup

---

## 📌 NEXT STEPS (OPTIONAL)

Fitur tambahan yang bisa dikembangkan di masa depan:

1. **Password reset untuk organisasi**
2. **Notifikasi email saat file diupload**
3. **Export all files sebagai ZIP**
4. **Edit keterangan file**
5. **File version history**
6. **Advanced filtering & search**
7. **File preview untuk PDF/Image**
8. **Audit log untuk semua aktivitas**

---

**Status: ✅ IMPLEMENTASI SELESAI & SIAP DIGUNAKAN**

Tanggal: 2026-09-24
