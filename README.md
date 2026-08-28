# Sistem Aspirasi MPK - Flask + SQLite

Sistem manajemen aspirasi siswa untuk MPK MAS Assalafiyyah menggunakan Flask framework dan SQLite database.

## 📋 Fitur

### Form Aspirasi (Publik)
- ✅ Pilih gender (Putra/Putri)
- ✅ Input nama, kelas, gender, kategori, deskripsi
- ✅ Validasi semua field wajib diisi
- ✅ Kirim data ke database SQLite
- ✅ Loading animation & success modal
- ✅ Responsive design

### Dashboard Admin (Login Required)
- ✅ Sistem login dengan Flask-Login
- ✅ Lihat semua aspirasi
- ✅ Filter berdasarkan status (Pending, Diproses, Selesai)
- ✅ Update status aspirasi
- ✅ Hapus aspirasi
- ✅ Realtime counter
- ✅ Responsive table

### Database
- **Engine:** SQLite3
- **ORM:** SQLAlchemy
- **Tabel:**
  - `aspirasi`: id, nama, kelas, gender, kategori, deskripsi, status, created_at
  - `admin`: id, username, password (hashed), created_at

## 📁 Struktur Project

```
MPKFULL/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── venv/                 # Virtual environment
├── templates/            # HTML templates (Flask Jinja2)
│   ├── index.html       # Landing page
│   ├── login.html       # Login admin
│   ├── krisisan.html    # Form aspirasi
│   └── dashboard.html   # Dashboard admin
├── static/              # Static files (CSS, JS, Images)
│   ├── assets/
│   │   ├── picture/
│   │   └── audio/
│   └── krisismpk.css
└── data/                # SQLite database
    └── aspirasi.db      # Database (auto-created)
```

## 🚀 Cara Setup & Menjalankan

### 1. Persyaratan Sistem
- Python 3.8 atau lebih tinggi
- pip (Python package installer)

### 2. Instalasi

**Clone atau download project:**
```bash
cd D:\belajar-web\MPKFULL
```

**Buat virtual environment:**
```bash
python -m venv venv
```

**Aktivasi virtual environment:**

Windows (PowerShell):
```bash
.\venv\Scripts\activate
```

Windows (CMD):
```bash
venv\Scripts\activate.bat
```

Linux/Mac:
```bash
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```bash
python app.py
```

Server akan berjalan di: `http://127.0.0.1:5000`

Output yang muncul:
```
Database created at: D:\belajar-web\MPKFULL\data\aspirasi.db
Default admin - username: admin, password: admin123
 * Running on http://127.0.0.1:5000
```

### 4. Akses Aplikasi

- **Landing Page:** http://127.0.0.1:5000/
- **Form Aspirasi:** http://127.0.0.1:5000/krisisan
- **Login Admin:** http://127.0.0.1:5000/login
- **Dashboard Admin:** http://127.0.0.1:5000/dashboard (perlu login)

## 🔐 Kredensial Admin Default

```
Username: admin
Password: admin123
```

⚠️ **PENTING:** Ganti password default setelah deployment!

## 🛣️ API Endpoints

| Endpoint | Method | Autentikasi | Keterangan |
|----------|--------|-------------|------------|
| `/` | GET | ❌ | Landing page |
| `/krisisan` | GET | ❌ | Form aspirasi siswa |
| `/login` | GET/POST | ❌ | Login admin |
| `/logout` | GET | ✅ | Logout admin |
| `/dashboard` | GET | ✅ | Dashboard admin |
| `/api/aspirasi` | POST | ❌ | Submit aspirasi baru |
| `/api/aspirasi` | GET | ✅ | Ambil semua aspirasi |
| `/api/aspirasi/<id>/status` | PUT | ✅ | Update status aspirasi |
| `/api/aspirasi/<id>` | DELETE | ✅ | Hapus aspirasi |
| `/api/check-auth` | GET | ✅ | Cek status autentikasi |

## 📦 Dependencies

```
flask==3.1.3
flask-sqlalchemy==3.1.1
flask-login==0.6.3
```

Install dengan:
```bash
pip install -r requirements.txt
```

## 🗄️ Database Schema

### Tabel: aspirasi
```sql
CREATE TABLE aspirasi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    kelas TEXT NOT NULL,
    gender TEXT NOT NULL,
    kategori TEXT NOT NULL,
    deskripsi TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabel: admin
```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- Hashed with pbkdf2:sha256
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

### 1. Test Form Aspirasi
1. Buka http://127.0.0.1:5000/krisisan
2. Pilih gender (Putra/Putri)
3. Isi semua field form
4. Submit
5. Cek success modal

### 2. Test Dashboard Admin
1. Buka http://127.0.0.1:5000/login
2. Login dengan `admin` / `admin123`
3. Lihat data aspirasi di dashboard
4. Test filter status
5. Test update status & delete

### 3. Test API
```bash
# Submit aspirasi (POST)
curl -X POST http://127.0.0.1:5000/api/aspirasi \
  -H "Content-Type: application/json" \
  -d '{"nama":"Test User","kelas":"10A","gender":"Putra","kategori":"Akademik","deskripsi":"Test aspirasi"}'

# Get semua aspirasi (GET - perlu login)
curl http://127.0.0.1:5000/api/aspirasi
```

## 🚨 Troubleshooting

### Error: "unable to open database file"
**Solusi:**
- Pastikan folder `data/` ada
- Cek permission folder (harus writable)
- Restart Flask app

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solusi:**
```bash
# Pastikan venv aktif
.\venv\Scripts\activate

# Install ulang dependencies
pip install -r requirements.txt
```

### Dashboard tidak bisa diakses (redirect ke login)
**Solusi:**
- Pastikan sudah login di `/login`
- Cek Flask session cookie
- Clear browser cache & cookies

### Data aspirasi tidak muncul
**Solusi:**
- Buka browser DevTools (F12) > Console
- Cek error message
- Pastikan sudah login sebagai admin
- Test API endpoint langsung

### Port 5000 sudah digunakan
**Solusi:**
Edit `app.py` baris terakhir:
```python
app.run(debug=True, port=5001)  # Ganti port
```

## 🔒 Keamanan

### Production Deployment
Sebelum deploy ke production:

1. **Ganti Secret Key:**
```python
app.config['SECRET_KEY'] = 'your-random-secret-key-here'
```

2. **Nonaktifkan Debug Mode:**
```python
app.run(debug=False, port=5000)
```

3. **Gunakan Production Server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Ganti Password Admin Default**

5. **Setup HTTPS**

6. **Backup Database Berkala**

## 💾 Backup Database

Database SQLite adalah single file: `data/aspirasi.db`

**Backup manual:**
```bash
# Copy database
copy data\aspirasi.db data\aspirasi_backup_2026-08-28.db
```

**Backup otomatis (Windows Task Scheduler / Linux Cron):**
```bash
# Script backup (backup_db.bat)
@echo off
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%
copy data\aspirasi.db backup\aspirasi_%timestamp%.db
```

**Export ke Excel:**
- Download [DB Browser for SQLite](https://sqlitebrowser.org/)
- Buka `aspirasi.db`
- Export table ke CSV/Excel

## 🌐 Deploy ke Hosting

### Option 1: PythonAnywhere (Gratis)
1. Daftar di https://www.pythonanywhere.com
2. Upload files
3. Setup virtualenv
4. Configure WSGI file
5. Reload web app

### Option 2: Heroku
1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn app:app
```
3. Deploy:
```bash
heroku create mpk-aspirasi
git push heroku main
```

### Option 3: VPS (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Setup app
git clone <repo>
cd MPKFULL
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/mpk.service

# Setup nginx reverse proxy
sudo nano /etc/nginx/sites-available/mpk

# Start service
sudo systemctl start mpk
sudo systemctl enable mpk
```

## 📝 Changelog

### Version 2.0 (2026-08-28)
- ✅ Migrasi dari PHP ke Flask framework
- ✅ Implementasi SQLAlchemy ORM
- ✅ Sistem autentikasi dengan Flask-Login
- ✅ Restructure project dengan templates dan static folders
- ✅ Virtual environment untuk dependency management
- ✅ RESTful API endpoints

### Version 1.0 (2026-08-27)
- ✅ Form aspirasi dengan PHP
- ✅ Dashboard admin sederhana
- ✅ SQLite database
- ✅ CRUD operations

## 📞 Kontak

Untuk pertanyaan, bug report, atau bantuan:
- Email: mpkmasassalafiyyah@gmail.com
- Instagram: [@maassalafiyyahmlangi](https://www.instagram.com/maassalafiyyahmlangi/)

---

**© 2024 MPK MAS ASSALAFIYYAH**
