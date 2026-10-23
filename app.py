"""
Sistem Penyewaan Alat Pendakian & Outdoor
Aplikasi Flask untuk manajemen penyewaan alat outdoor

Fitur:
- CRUD Manajemen Alat
- CRUD Manajemen Penyewa
- Transaksi Penyewaan dengan kalkulasi otomatis
- Pengembalian dengan perhitungan denda keterlambatan
- Laporan Penyewaan

Author: Admin
Date: 2026
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.database import db, Alat, Penyewa, Sewa
from routes.alat import alat_bp
from routes.penyewa import penyewa_bp
from routes.sewa import sewa_bp
from routes.laporan import laporan_bp
import os
import tempfile

# Inisialisasi Flask App
app = Flask(__name__)

# Konfigurasi Database
basedir = os.path.abspath(os.path.dirname(__file__))
# DATABASE_URL dipakai untuk database production (misalnya PostgreSQL dari
# Vercel/Neon). SQLite hanya dipakai sebagai fallback development.
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Beberapa provider masih mengirim URL dengan skema postgres:// lama.
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
elif os.environ.get('VERCEL'):
    # Filesystem deployment Vercel bersifat read-only; /tmp hanya untuk
    # fallback sementara agar function tidak gagal saat DATABASE_URL belum ada.
    database_url = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'sewa_alat.db')
else:
    database_url = 'sqlite:///' + os.path.join(basedir, 'sewa_alat.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-this-secret')
# Admin credentials (default). Ubah melalui environment untuk production.
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Inisialisasi Database
db.init_app(app)

# Vercel memuat app.py sebagai serverless function dan tidak menjalankan
# blok `if __name__ == '__main__'`. Pastikan schema tersedia saat function
# pertama kali dipanggil.
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(alat_bp)
app.register_blueprint(penyewa_bp)
app.register_blueprint(sewa_bp)
app.register_blueprint(laporan_bp)


@app.before_request
def require_login():
    """Require admin login for most routes.

    Exceptions: static files and the login/logout endpoints.
    """
    # Allow static files, login and error handlers
    endpoint = request.endpoint or ''
    if endpoint.startswith('static'):
        return
    if endpoint in ('login', 'logout'):
        return

    # If not logged in, redirect to login page
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple admin login (session-based)."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash('Login berhasil. Selamat datang, Admin!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username atau password salah.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Anda telah logout.', 'success')
    return redirect(url_for('login'))


@app.route('/')
def home():
    """Halaman utama/dashboard"""
    total_alat = Alat.query.count()
    total_penyewa = Penyewa.query.count()
    total_sewa = Sewa.query.count()
    total_sewa_aktif = Sewa.query.filter_by(status='aktif').count()
    
    return render_template('index.html',
                         total_alat=total_alat,
                         total_penyewa=total_penyewa,
                         total_sewa=total_sewa,
                         total_sewa_aktif=total_sewa_aktif)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 error"""
    return render_template('500.html'), 500


# Context processor untuk format currency
@app.template_filter('format_currency')
def format_currency(value):
    """Format angka menjadi currency Indonesia"""
    if value is None:
        return 'Rp0'
    return f'Rp{int(value):,}'.replace(',', '.')


if __name__ == '__main__':
    # Buat database dan tabel jika belum ada
    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully!")
    
    # Jalankan aplikasi
    print("=" * 50)
    print("Sistem Penyewaan Alat Pendakian & Outdoor")
    print("=" * 50)
    print("Server running on http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='localhost', port=5000)
