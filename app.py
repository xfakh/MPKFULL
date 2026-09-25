from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mpk-secret-key-2026'

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, 'aspirasi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(data_dir, 'uploads', 'organization')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'txt'}

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
    
    def get_id(self):
        return f'admin_{self.id}'

class Aspirasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Organization(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    files = db.relationship('OrganizationFile', backref='organization', lazy=True, cascade='all, delete-orphan')
    
    def get_id(self):
        return f'org_{self.id}'

class OrganizationFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='uploaded')
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith('admin_'):
        return Admin.query.get(int(user_id.replace('admin_', '')))
    elif user_id.startswith('org_'):
        return Organization.query.get(int(user_id.replace('org_', '')))
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'role') or current_user.role != 'admin':
            return jsonify({'success': False, 'message': 'Akses ditolak. Hanya admin yang dapat melakukan ini.'}), 403
        return f(*args, **kwargs)
    return decorated_function

def organization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'username'):
            return jsonify({'success': False, 'message': 'Akses ditolak. Hanya organisasi yang dapat melakukan ini.'}), 403
        return f(*args, **kwargs)
    return decorated_function

def create_default_admin():
    if Admin.query.count() == 0:
        hashed_password = generate_password_hash('mpkassalafiyyah', method='pbkdf2:sha256')
        admin = Admin(username='admin', password=hashed_password, role='admin')
        db.session.add(admin)
        db.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/krisisan')
def krisisan():
    return render_template('krisisan.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Check if user is admin or organization
        if hasattr(current_user, 'role'):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('org_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username dan password wajib diisi', 'error')
            return redirect(url_for('login'))
        
        # Try login as Admin first
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return jsonify({'success': True, 'message': 'Login berhasil', 'redirect': url_for('dashboard')})
        
        # Try login as Organization
        org = Organization.query.filter_by(username=username).first()
        if org and check_password_hash(org.password, password):
            login_user(org)
            return jsonify({'success': True, 'message': 'Login berhasil', 'redirect': url_for('org_dashboard')})
        
        # Login failed
        flash('Username atau password salah', 'error')
        return redirect(url_for('login'))
    
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

@app.route('/org/login', methods=['GET', 'POST'])
def org_login():
    # Redirect to unified login page
    return redirect(url_for('login'))

@app.route('/org/logout')
@login_required
def org_logout():
    logout_user()
    return redirect(url_for('org_login'))

@app.route('/org/dashboard')
@login_required
def org_dashboard():
    if not hasattr(current_user, 'username'):
        flash('Akses ditolak. Hanya organisasi yang dapat mengakses halaman ini.', 'error')
        return redirect(url_for('org_login'))
    return render_template('org_dashboard.html')

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
        user_type = 'admin' if hasattr(current_user, 'role') else 'organization'
        
        response_data = {
            'id': current_user.id,
            'username': current_user.username,
            'user_type': user_type
        }
        
        if user_type == 'admin':
            response_data['role'] = current_user.role
        else:
            response_data['name'] = current_user.name
        
        return jsonify({
            'success': True,
            'authenticated': True,
            'admin': response_data
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

@app.route('/api/organizations', methods=['GET'])
@login_required
@admin_required
def get_organizations():
    organizations = Organization.query.order_by(Organization.created_at.desc()).all()
    data = [{
        'id': org.id,
        'name': org.name,
        'username': org.username,
        'email': org.email,
        'status': org.status,
        'file_count': len(org.files),
        'created_at': org.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for org in organizations]
    return jsonify({'success': True, 'data': data})

@app.route('/api/organizations', methods=['POST'])
@login_required
@admin_required
def create_organization():
    data = request.get_json()
    
    required_fields = ['name', 'username', 'password', 'email']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f'{field} wajib diisi'}), 400
    
    if Organization.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Username sudah digunakan'}), 400
    
    if Organization.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email sudah digunakan'}), 400
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    org = Organization(
        name=data['name'],
        username=data['username'],
        password=hashed_password,
        email=data['email']
    )
    
    db.session.add(org)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Organisasi berhasil dibuat',
        'organization': {
            'id': org.id,
            'name': org.name,
            'username': org.username,
            'email': org.email,
            'status': org.status
        }
    })

@app.route('/api/organizations/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_organization(id):
    org = Organization.query.get(id)
    
    if not org:
        return jsonify({'success': False, 'message': 'Organisasi tidak ditemukan'}), 404
    
    db.session.delete(org)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Organisasi berhasil dihapus'})

@app.route('/api/organizations/<int:id>/toggle-status', methods=['PUT'])
@login_required
@admin_required
def toggle_organization_status(id):
    org = Organization.query.get(id)
    
    if not org:
        return jsonify({'success': False, 'message': 'Organisasi tidak ditemukan'}), 404
    
    # Toggle status
    org.status = 'inactive' if org.status == 'active' else 'active'
    db.session.commit()
    
    status_text = 'diaktifkan' if org.status == 'active' else 'dinonaktifkan'
    return jsonify({
        'success': True, 
        'message': f'Organisasi {org.name} berhasil {status_text}',
        'status': org.status
    })

@app.route('/api/org/admin/files/<int:file_id>/status', methods=['PUT'])
@login_required
@admin_required
def update_file_status(file_id):
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'success': False, 'message': 'Status tidak boleh kosong'}), 400
    
    file = OrganizationFile.query.get(file_id)
    
    if not file:
        return jsonify({'success': False, 'message': 'File tidak ditemukan'}), 404
    
    allowed_statuses = ['pending', 'verified', 'rejected']
    if data['status'] not in allowed_statuses:
        return jsonify({'success': False, 'message': 'Status tidak valid'}), 400
    
    file.status = data['status']
    db.session.commit()
    
    status_text = {
        'pending': 'menunggu verifikasi',
        'verified': 'terverifikasi',
        'rejected': 'ditolak'
    }
    
    return jsonify({
        'success': True,
        'message': f'File berhasil diubah menjadi {status_text[data["status"]]}',
        'status': file.status
    })

@app.route('/api/org/admin/files/<int:file_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_org_file_admin(file_id):
    file = OrganizationFile.query.get(file_id)
    
    if not file:
        return jsonify({'success': False, 'message': 'File tidak ditemukan'}), 404
    
    # Hapus file fisik
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(file)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'File berhasil dihapus'})

@app.route('/api/org/files', methods=['GET'])
@login_required
@organization_required
def get_org_files():
    if not hasattr(current_user, 'id'):
        return jsonify({'success': False, 'message': 'Akses ditolak'}), 403
    
    files = OrganizationFile.query.filter_by(organization_id=current_user.id).order_by(OrganizationFile.uploaded_at.desc()).all()
    data = [{
        'id': f.id,
        'file_name': f.file_name,
        'file_type': f.file_type,
        'file_size': f.file_size,
        'description': f.description,
        'status': f.status,
        'uploaded_at': f.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
    } for f in files]
    
    return jsonify({'success': True, 'data': data, 'count': len(data)})

@app.route('/api/org/info', methods=['GET'])
@login_required
@organization_required
def get_org_info():
    if not hasattr(current_user, 'name'):
        return jsonify({'success': False, 'message': 'Akses ditolak'}), 403
    
    return jsonify({
        'success': True,
        'organization': {
            'id': current_user.id,
            'name': current_user.name,
            'username': current_user.username,
            'email': current_user.email
        }
    })

@app.route('/api/org/upload', methods=['POST'])
@login_required
@organization_required
def upload_org_file():
    if not hasattr(current_user, 'id'):
        return jsonify({'success': False, 'message': 'Akses ditolak'}), 403
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'File tidak ditemukan'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'File tidak dipilih'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Tipe file tidak diizinkan'}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        description = request.form.get('description', '')
        
        org_file = OrganizationFile(
            organization_id=current_user.id,
            file_name=filename,
            file_path=unique_filename,
            file_type=file_ext,
            file_size=file_size,
            description=description
        )
        
        db.session.add(org_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'File berhasil diupload',
            'file': {
                'id': org_file.id,
                'file_name': org_file.file_name,
                'file_type': org_file.file_type,
                'file_size': org_file.file_size,
                'uploaded_at': org_file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Gagal upload file: {str(e)}'}), 500

@app.route('/api/org/files/<int:file_id>', methods=['DELETE'])
@login_required
@organization_required
def delete_org_file(file_id):
    if not hasattr(current_user, 'id'):
        return jsonify({'success': False, 'message': 'Akses ditolak'}), 403
    
    org_file = OrganizationFile.query.get(file_id)
    
    if not org_file:
        return jsonify({'success': False, 'message': 'File tidak ditemukan'}), 404
    
    if org_file.organization_id != current_user.id:
        return jsonify({'success': False, 'message': 'Anda tidak berhak menghapus file ini'}), 403
    
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], org_file.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(org_file)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'File berhasil dihapus'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Gagal menghapus file: {str(e)}'}), 500

@app.route('/api/org/admin/organizations', methods=['GET'])
@login_required
@admin_required
def admin_get_org_files():
    org_id = request.args.get('org_id')
    
    if org_id:
        files = OrganizationFile.query.filter_by(organization_id=org_id).order_by(OrganizationFile.uploaded_at.desc()).all()
    else:
        files = OrganizationFile.query.order_by(OrganizationFile.uploaded_at.desc()).all()
    
    data = [{
        'id': f.id,
        'organization_id': f.organization_id,
        'organization_name': f.organization.name,
        'file_name': f.file_name,
        'file_type': f.file_type,
        'file_size': f.file_size,
        'description': f.description,
        'status': f.status,
        'uploaded_at': f.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
    } for f in files]
    
    return jsonify({'success': True, 'data': data, 'count': len(data)})

@app.route('/api/org/admin/download/<int:file_id>')
@login_required
@admin_required
def admin_download_file(file_id):
    from flask import send_from_directory
    
    org_file = OrganizationFile.query.get(file_id)
    
    if not org_file:
        return jsonify({'success': False, 'message': 'File tidak ditemukan'}), 404
    
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], org_file.file_path, as_attachment=True, download_name=org_file.file_name)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Gagal download file: {str(e)}'}), 500


@app.route('/api/dashboard/stats')
@login_required
@admin_required
def get_dashboard_stats():
    """
    API endpoint untuk mendapatkan statistics dashboard admin
    Returns: stats cards data, trend data, kategori distribution, top organizations
    """
    try:
        # Get current date range
        end_date = datetime.utcnow()
        start_date_6m = end_date.replace(month=max(1, end_date.month - 6)) if end_date.month > 6 else \
            datetime(end_date.year - 1, end_date.month + 6, end_date.day)
        
        start_date_30d = end_date.replace(day=max(1, end_date.day - 30))
        start_date_7d = end_date.replace(day=max(1, end_date.day - 7))
        
        # Stats Cards - Current Period
        total_current = Aspirasi.query.count()
        pending_current = Aspirasi.query.filter_by(status='pending').count()
        diproses_current = Aspirasi.query.filter_by(status='diproses').count()
        selesai_current = Aspirasi.query.filter_by(status='selesai').count()
        
        # Stats Cards - Previous Period (for trend comparison)
        total_prev = Aspirasi.query.filter(Aspirasi.created_at < start_date_30d).count()
        pending_prev = Aspirasi.query.filter(Aspirasi.created_at < start_date_30d, Aspirasi.status == 'pending').count()
        diproses_prev = Aspirasi.query.filter(Aspirasi.created_at < start_date_30d, Aspirasi.status == 'diproses').count()
        selesai_prev = Aspirasi.query.filter(Aspirasi.created_at < start_date_30d, Aspirasi.status == 'selesai').count()
        
        # Calculate trends (percentage change)
        def calc_trend(current, prev):
            if prev == 0:
                return 0
            return ((current - prev) / prev) * 100
        
        # 6-Month Trend Data (Line Chart)
        trend_data = []
        for i in range(6, -1, -1):
            month_date = end_date.replace(month=max(1, end_date.month - i)) if end_date.month > i else \
                datetime(end_date.year - 1, end_date.month + 12 - i, end_date.day)
            month_start = datetime(month_date.year, month_date.month, 1)
            month_end = datetime(month_date.year, month_date.month + 1, 1) if month_date.month < 12 else \
                datetime(month_date.year + 1, 1, 1)
            
            month_aspirasi = Aspirasi.query.filter(
                Aspirasi.created_at >= month_start,
                Aspirasi.created_at < month_end
            ).all()
            
            month_total = len(month_aspirasi)
            month_selesai = len([a for a in month_aspirasi if a.status == 'selesai'])
            
            trend_data.append({
                'label': month_date.strftime('%B %Y'),
                'total': month_total,
                'selesai': month_selesai
            })
        
        # Kategori Distribution (Pie Chart)
        kategori_distribution = []
        kategori_data = db.session.query(
            Aspirasi.kategori,
            db.func.count(Aspirasi.id).label('jumlah')
        ).group_by(Aspirasi.kategori).all()
        
        for kategori, jumlah in kategori_data:
            kategori_distribution.append({
                'kategori': kategori,
                'jumlah': jumlah
            })
        
        # Top 10 Organizations by File Count (Bar Chart)
        organi_data = db.session.query(
            Organization.name,
            db.func.count(OrganizationFile.id).label('file_count')
        ).join(OrganizationFile).group_by(Organization.id).order_by(db.desc('file_count')).limit(10).all()
        
        organi = []
        for name, file_count in organi_data:
            organi.append({
                'name': name,
                'file_count': file_count
            })
        
        stats = {
            'total': total_current,
            'total_trend': calc_trend(total_current, total_prev),
            'pending': pending_current,
            'pending_trend': calc_trend(pending_current, pending_prev),
            'diproses': diproses_current,
            'diproses_trend': calc_trend(diproses_current, diproses_prev),
            'selesai': selesai_current,
            'selesai_trend': calc_trend(selesai_current, selesai_prev)
        }
        
        return jsonify({
            'success': True,
            'data': {
                'stats': stats,
                'trend_data': trend_data,
                'kategori_distribution': kategori_distribution,
                'organi': organi
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
        print(f"Database created at: {db_path}")
        print("Default admin - username: admin, password: mpkassalafiyyah")
    
    app.run(debug=True, port=5000)
