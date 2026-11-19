# 🚀 CARA MENJALANKAN & TESTING SISTEM ORGANISASI

## 📋 Prerequisites

- Python 3.8+
- Virtual environment sudah disetup
- Dependencies sudah diinstall

## ⚡ Quick Start

### 1. Aktifkan Virtual Environment

```bash
source venv/bin/activate
```

### 2. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: **http://127.0.0.1:5000**

---

## 🧪 PANDUAN TESTING LENGKAP

### Test 1: Fitur Aspirasi Siswa (Existing - Harus Tetap Berfungsi)

#### ✅ Test Form Aspirasi
1. Buka: **http://127.0.0.1:5000/krisisan**
2. Pilih gender: Putra atau Putri
3. Isi form:
   - Nama: John Doe
   - Kelas: (pilih dari dropdown)
   - Gender: (auto-fill dari pilihan)
   - Kategori: Akademik
   - Deskripsi: Test aspirasi sistem
4. Klik "Kirim Aspirasi"
5. **Expected:** Modal sukses muncul, data tersimpan

#### ✅ Test Dashboard Admin Aspirasi
1. Buka: **http://127.0.0.1:5000/login**
2. Login:
   - Username: `admin`
   - Password: `mpkassalafiyyah`
3. Klik Login
4. **Expected:** Redirect ke dashboard, lihat aspirasi yang baru disubmit
5. Test filter, update status, delete aspirasi
6. **Expected:** Semua fungsi berjalan normal

---

### Test 2: Login Organisasi (New Feature)

#### ✅ Test Login Berhasil
1. Buka: **http://127.0.0.1:5000/org/login**
2. Login dengan salah satu organisasi:
   - Username: `osis`
   - Password: `osis123`
3. Klik "Login Organisasi"
4. **Expected:** Redirect ke dashboard organisasi

#### ✅ Test Login Gagal
1. Buka: **http://127.0.0.1:5000/org/login**
2. Login dengan credential salah:
   - Username: `osis`
   - Password: `salah123`
3. **Expected:** Error message "Username atau password salah"

#### ✅ Test Akses Tanpa Login
1. Logout jika sudah login
2. Coba akses langsung: **http://127.0.0.1:5000/org/dashboard**
3. **Expected:** Redirect ke login page

---

### Test 3: Dashboard Organisasi (New Feature)

#### ✅ Test Dashboard View
1. Login sebagai organisasi (osis/osis123)
2. **Expected:** Melihat:
   - Nama organisasi di sidebar
   - Stats cards (Total File, Total Upload, Total Size)
   - File terbaru (kosong jika belum ada upload)

#### ✅ Test Upload File
1. Di dashboard, klik "File Upload" di sidebar
2. Klik area drop zone atau drag file
3. Pilih file (contoh: test.pdf)
4. Isi keterangan: "Laporan kegiatan bulan September"
5. Klik "Upload File"
6. **Expected:** 
   - Toast success muncul
   - File muncul di tabel "Riwayat Upload"
   - Stats counter bertambah

#### ✅ Test Upload File Invalid
1. Coba upload file dengan ekstensi tidak diizinkan (.exe, .zip, dll)
2. **Expected:** Error "Tipe file tidak diizinkan"

#### ✅ Test Upload File Terlalu Besar
1. Coba upload file > 16MB
2. **Expected:** Error "File tidak boleh lebih besar dari 16MB"

#### ✅ Test Delete File
1. Setelah upload file, klik icon trash pada file
2. Confirm delete
3. **Expected:** File terhapus, stats berkurang

#### ✅ Test Logout Organisasi
1. Klik "Logout" di sidebar
2. **Expected:** Redirect ke login page organisasi

---

### Test 4: Dashboard Admin Monitoring Organisasi (New Feature)

#### ✅ Test Akses Dashboard Admin Org
1. Login sebagai admin (admin/mpkassalafiyyah)
2. Akses: **http://127.0.0.1:5000/org/admin/dashboard**
3. **Expected:** Melihat dashboard monitoring organisasi

#### ✅ Test View List Organisasi
1. Di dashboard admin organisasi, tab "Organisasi"
2. **Expected:** Melihat tabel dengan 5 organisasi:
   - OSIS, Rohis, Pramuka, PMR, Paskibra
   - Username, email, jumlah file, status

#### ✅ Test Tambah Organisasi Baru
1. Klik "Tambah Organisasi"
2. Isi form:
   - Nama: Ekstrakurikuler Futsal
   - Username: futsal
   - Email: futsal@example.com
   - Password: futsal123
3. Klik "Simpan"
4. **Expected:** 
   - Modal tertutup
   - Organisasi baru muncul di tabel
   - Total organisasi bertambah

#### ✅ Test Tambah Organisasi Duplikat Username
1. Klik "Tambah Organisasi"
2. Isi dengan username yang sudah ada (contoh: osis)
3. **Expected:** Error "Username sudah digunakan"

#### ✅ Test View File Organisasi
1. Klik tab "File Organisasi"
2. **Expected:** Melihat semua file dari semua organisasi
3. Test filter berdasarkan organisasi
4. **Expected:** File ter-filter sesuai organisasi yang dipilih

#### ✅ Test Download File
1. Di tab "File Organisasi", klik icon download pada file
2. **Expected:** File ter-download dengan nama file asli

#### ✅ Test Delete Organisasi
1. Di tab "Organisasi", klik icon trash pada salah satu organisasi
2. Confirm delete
3. **Expected:** 
   - Organisasi terhapus
   - Semua file terkait juga terhapus (cascade delete)

---

### Test 5: Authorization & Security (Critical)

#### ✅ Test Isolasi Data Organisasi
1. Login sebagai organisasi A (osis/osis123)
2. Upload beberapa file
3. Logout, login sebagai organisasi B (rohis/rohis123)
4. **Expected:** Hanya melihat file milik organisasi B, tidak melihat file organisasi A

#### ✅ Test Akses Cross-Organization
1. Login sebagai organisasi A
2. Coba hapus file dengan ID dari organisasi B (manual API call)
3. **Expected:** Error 403 Forbidden atau error authorization

#### ✅ Test Non-Admin Access Dashboard Admin
1. Login sebagai organisasi (bukan admin)
2. Coba akses: **http://127.0.0.1:5000/org/admin/dashboard**
3. **Expected:** Access denied atau redirect

#### ✅ Test Password Hashing
1. Check database manually:
```bash
sqlite3 data/aspirasi.db "SELECT username, password FROM organization LIMIT 1;"
```
2. **Expected:** Password ter-hash, bukan plaintext

---

### Test 6: Integrasi & Compatibility

#### ✅ Test Dual Login System
1. Buka 2 browser/incognito window
2. Window 1: Login sebagai admin di /login
3. Window 2: Login sebagai organisasi di /org/login
4. **Expected:** Kedua session berjalan independen

#### ✅ Test Navigation
1. Login sebagai admin
2. Akses dashboard aspirasi: **http://127.0.0.1:5000/dashboard**
3. **Expected:** Dashboard aspirasi berfungsi normal
4. Akses dashboard organisasi: **http://127.0.0.1:5000/org/admin/dashboard**
5. **Expected:** Dashboard organisasi berfungsi normal
6. **Expected:** Bisa switch bolak-balik tanpa error

#### ✅ Test Data Integrity
1. Submit aspirasi siswa
2. Upload file organisasi
3. Check database:
```bash
sqlite3 data/aspirasi.db "SELECT COUNT(*) FROM aspirasi;"
sqlite3 data/aspirasi.db "SELECT COUNT(*) FROM organization_file;"
```
4. **Expected:** Data tersimpan di tabel yang benar, tidak bercampur

---

## 📊 CHECKLIST TESTING

### Fitur Lama (Harus Tetap Berfungsi)
- [ ] Landing page (/): Load tanpa error
- [ ] Form aspirasi (/krisisan): Submit berhasil
- [ ] Admin login (/login): Login berhasil
- [ ] Dashboard admin aspirasi (/dashboard): Berfungsi normal
- [ ] Filter/update/delete aspirasi: Berfungsi normal
- [ ] User management admin: Berfungsi normal

### Fitur Baru (Organisasi)
- [ ] Organization login (/org/login): Login berhasil
- [ ] Organization dashboard (/org/dashboard): Load dengan benar
- [ ] Upload file: Berhasil dengan validasi
- [ ] View riwayat file: Hanya file milik org
- [ ] Delete file: Berhasil
- [ ] Admin dashboard org (/org/admin/dashboard): Load dengan benar
- [ ] View all organizations: Menampilkan semua org
- [ ] Create organization: Berhasil dengan validasi
- [ ] View all files: Menampilkan file semua org
- [ ] Download file: Berhasil
- [ ] Delete organization: Berhasil dengan cascade

### Security
- [ ] Password di-hash di database
- [ ] Organisasi tidak bisa akses file org lain
- [ ] Organisasi tidak bisa akses dashboard admin
- [ ] Non-login tidak bisa upload
- [ ] File type validation berfungsi
- [ ] File size validation berfungsi

### Integration
- [ ] Data aspirasi tidak terganggu
- [ ] Data organisasi terpisah dari aspirasi
- [ ] Dual login system berfungsi
- [ ] Navigation antar dashboard lancar

---

## 🐛 DEBUGGING

### Check Database
```bash
# Lihat semua tabel
sqlite3 data/aspirasi.db ".tables"

# Lihat struktur tabel organization
sqlite3 data/aspirasi.db ".schema organization"

# Lihat data organisasi
sqlite3 data/aspirasi.db "SELECT * FROM organization;"

# Lihat data file
sqlite3 data/aspirasi.db "SELECT * FROM organization_file;"

# Lihat data aspirasi
sqlite3 data/aspirasi.db "SELECT COUNT(*) FROM aspirasi;"
```

### Check Upload Folder
```bash
# Pastikan folder ada
ls -la data/uploads/organization/

# Check file yang sudah diupload
ls -lh data/uploads/organization/
```

### Check Logs
```bash
# Jalankan aplikasi dengan verbose mode
python app.py
# Lihat output di terminal untuk error
```

---

## 🎯 HASIL TESTING YANG DIHARAPKAN

Setelah semua testing selesai:

✅ **Semua fitur lama berfungsi normal (aspirasi siswa)**
✅ **Semua fitur baru berfungsi (sistem organisasi)**
✅ **Data terpisah dengan baik**
✅ **Security checks passed**
✅ **No breaking changes**

---

## 📞 TROUBLESHOOTING

**Problem:** Port 5000 sudah digunakan
```bash
# Cari process yang pakai port 5000
lsof -i :5000
# Kill process atau ganti port di app.py
```

**Problem:** Module not found
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

**Problem:** Database error
```bash
# Recreate database
rm data/aspirasi.db
python app.py
# Akan auto create tables
```

**Problem:** Upload folder permission denied
```bash
# Set permission
chmod -R 755 data/uploads/
```

---

## ✅ CHECKLIST SEBELUM PRODUCTION

- [ ] Ganti SECRET_KEY di app.py
- [ ] Ganti password default admin
- [ ] Setup environment variables
- [ ] Enable HTTPS
- [ ] Setup backup database otomatis
- [ ] Review file upload limits
- [ ] Setup monitoring & logging
- [ ] Test di production environment

---

**Happy Testing! 🚀**
