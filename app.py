from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mpk-secret-key-2026'

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, 'aspirasi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini'
login_manager.login_message_category = 'info'

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='staff')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Aspirasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({'success': False, 'message': 'Akses ditolak. Hanya admin yang dapat melakukan ini.'}), 403
        return f(*args, **kwargs)
    return decorated_function

def create_default_admin():
    if Admin.query.count() == 0:
        hashed_password = generate_password_hash('mpkassalafiyyah', method='pbkdf2:sha256')
        admin = Admin(username='admin', password=hashed_password, role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/krisisan')
def krisisan():
    return render_template('krisisan.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# API Routes
@app.route('/api/aspirasi', methods=['POST'])
def save_aspirasi():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'Data tidak valid'}), 400
    
    required_fields = ['nama', 'kelas', 'gender', 'kategori', 'deskripsi']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f'Field {field} wajib diisi'}), 400
    
    aspirasi = Aspirasi(
        nama=data['nama'],
        kelas=data['kelas'],
        gender=data['gender'],
        kategori=data['kategori'],
        deskripsi=data['deskripsi']
    )
    
    db.session.add(aspirasi)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Aspirasi berhasil dikirim',
        'id': aspirasi.id
    })

@app.route('/api/aspirasi', methods=['GET'])
def get_aspirasi():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Tidak terautentikasi', 'authenticated': False}), 401
    status_filter = request.args.get('status')
    kelas_filter = request.args.get('kelas')
    kategori_filter = request.args.get('kategori')
    
    query = Aspirasi.query
    
    if status_filter and status_filter in ['pending', 'diproses', 'selesai']:
        query = query.filter_by(status=status_filter)
    
    if kelas_filter:
        query = query.filter_by(kelas=kelas_filter)
    
    if kategori_filter:
        query = query.filter_by(kategori=kategori_filter)
    
    aspirasi_list = query.order_by(Aspirasi.created_at.desc()).all()
    
    data = [{
        'id': a.id,
        'nama': a.nama,
        'kelas': a.kelas,
        'gender': a.gender,
        'kategori': a.kategori,
        'deskripsi': a.deskripsi,
        'status': a.status,
        'created_at': a.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for a in aspirasi_list]
    
    return jsonify({'success': True, 'data': data, 'count': len(data)})

@app.route('/api/aspirasi/<int:id>/status', methods=['PUT'])
def update_status(id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Tidak terautentikasi', 'authenticated': False}), 401
    
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'success': False, 'message': 'Status wajib diisi'}), 400
    
    if data['status'] not in ['pending', 'diproses', 'selesai']:
        return jsonify({'success': False, 'message': 'Status tidak valid'}), 400
    
    aspirasi = Aspirasi.query.get(id)
    
    if not aspirasi:
        return jsonify({'success': False, 'message': 'Aspirasi tidak ditemukan'}), 404
    
    aspirasi.status = data['status']
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Status berhasil diupdate'})

@app.route('/api/aspirasi/<int:id>', methods=['DELETE'])
def delete_aspirasi(id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Tidak terautentikasi', 'authenticated': False}), 401
    
    aspirasi = Aspirasi.query.get(id)
    
    if not aspirasi:
        return jsonify({'success': False, 'message': 'Aspirasi tidak ditemukan'}), 404
    
    db.session.delete(aspirasi)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Aspirasi berhasil dihapus'})

@app.route('/api/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'success': True,
            'authenticated': True,
            'admin': {
                'id': current_user.id,
                'username': current_user.username,
                'role': current_user.role
            }
        })
    else:
        return jsonify({
            'success': False,
            'authenticated': False,
            'message': 'Tidak terautentikasi'
        }), 401

@app.route('/api/admin/users', methods=['GET'])
@login_required
def get_admin_users():
    users = Admin.query.order_by(Admin.created_at.desc()).all()
    data = [{
        'id': u.id,
        'username': u.username,
        'role': u.role,
        'created_at': u.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for u in users]
    return jsonify({'success': True, 'data': data})

@app.route('/api/admin/users', methods=['POST'])
@login_required
@admin_required
def create_admin_user():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Username dan password wajib diisi'}), 400
    
    if Admin.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Username sudah digunakan'}), 400
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    role = data.get('role', 'staff')
    
    new_admin = Admin(username=data['username'], password=hashed_password, role=role)
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User berhasil ditambahkan',
        'user': {
            'id': new_admin.id,
            'username': new_admin.username,
            'role': new_admin.role
        }
    })

@app.route('/api/admin/users/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_admin_user(id):
    if current_user.id == id:
        return jsonify({'success': False, 'message': 'Tidak dapat menghapus akun sendiri'}), 400
    
    user = Admin.query.get(id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User berhasil dihapus'})

@app.route('/api/admin/users/<int:id>/reset-password', methods=['PUT'])
@login_required
@admin_required
def reset_admin_password(id):
    data = request.get_json()
    
    if not data or 'new_password' not in data:
        return jsonify({'success': False, 'message': 'Password baru wajib diisi'}), 400
    
    user = Admin.query.get(id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404
    
    hashed_password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    user.password = hashed_password
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password berhasil direset'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
        print(f"Database created at: {db_path}")
        print("Default admin - username: admin, password: mpkassalafiyyah")
    
    app.run(debug=True, port=5000)
