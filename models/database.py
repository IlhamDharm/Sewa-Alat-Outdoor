"""
Database initialization menggunakan Flask-SQLAlchemy
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Alat(db.Model):
    """
    Model untuk data alat pendakian
    Fields:
        - id: Primary key
        - nama: Nama alat
        - kategori: Kategori alat (tenda, sleeping bag, dll)
        - stok: Jumlah stok alat yang tersedia
        - harga_per_hari: Harga sewa per hari (dalam Rupiah)
        - kondisi: Kondisi alat (baik, rusak, rusak berat)
        - created_at: Timestamp pembuatan
    """
    __tablename__ = 'alat'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    stok = db.Column(db.Integer, nullable=False, default=0)
    harga_per_hari = db.Column(db.Integer, nullable=False)
    kondisi = db.Column(db.String(20), nullable=False, default='baik')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relasi ke DetailSewa
    detail_sewa = db.relationship('DetailSewa', backref='alat', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Alat {self.nama}>'


class User(db.Model):
    """Akun pelanggan untuk user panel."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    no_hp = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sewa = db.relationship('Sewa', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Penyewa(db.Model):
    """
    Model untuk data penyewa
    Fields:
        - id: Primary key
        - nama: Nama penyewa
        - no_hp: Nomor HP penyewa
        - alamat: Alamat penyewa
        - jaminan: Jaminan atau catatan jaminan (KTP, SIM, dll)
        - created_at: Timestamp pembuatan
    """
    __tablename__ = 'penyewa'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(15), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    jaminan = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relasi ke Sewa
    sewa = db.relationship('Sewa', backref='penyewa', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Penyewa {self.nama}>'


class Sewa(db.Model):
    """
    Model untuk transaksi penyewaan
    Fields:
        - id: Primary key
        - penyewa_id: Foreign key ke Penyewa
        - tanggal_sewa: Tanggal penyewaan dimulai
        - tanggal_rencana_kembali: Tanggal rencana pengembalian
        - tanggal_kembali_aktual: Tanggal pengembalian aktual (null jika belum dikembalikan)
        - total_biaya: Total biaya sewa
        - total_denda: Total denda keterlambatan
        - status: Status sewa (aktif, dikembalikan)
        - created_at: Timestamp pembuatan
    """
    __tablename__ = 'sewa'
    
    id = db.Column(db.Integer, primary_key=True)
    penyewa_id = db.Column(db.Integer, db.ForeignKey('penyewa.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    order_status = db.Column(db.String(20), nullable=False, default='menunggu')
    tanggal_sewa = db.Column(db.DateTime, nullable=False)
    tanggal_rencana_kembali = db.Column(db.DateTime, nullable=False)
    tanggal_kembali_aktual = db.Column(db.DateTime, nullable=True)
    total_biaya = db.Column(db.Integer, nullable=False, default=0)
    total_denda = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='aktif')  # aktif, dikembalikan
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relasi ke DetailSewa
    detail_sewa = db.relationship('DetailSewa', backref='sewa', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sewa {self.id} - Penyewa {self.penyewa_id}>'


class DetailSewa(db.Model):
    """
    Model untuk detail item dalam satu transaksi sewa
    Fields:
        - id: Primary key
        - sewa_id: Foreign key ke Sewa
        - alat_id: Foreign key ke Alat
        - jumlah: Jumlah alat yang disewa
        - harga_satuan: Harga per hari saat transaksi (stored untuk history)
        - subtotal: Total biaya untuk item ini (jumlah * harga_satuan * jumlah_hari)
    """
    __tablename__ = 'detail_sewa'
    
    id = db.Column(db.Integer, primary_key=True)
    sewa_id = db.Column(db.Integer, db.ForeignKey('sewa.id'), nullable=False)
    alat_id = db.Column(db.Integer, db.ForeignKey('alat.id'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False, default=1)
    harga_satuan = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f'<DetailSewa {self.id} - Sewa {self.sewa_id} - Alat {self.alat_id}>'
