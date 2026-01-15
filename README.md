# Sistem Penyewaan Alat Pendakian & Outdoor
# Flask Web Application

## Deskripsi
Aplikasi web berbasis Python Flask untuk manajemen sistem penyewaan alat pendakian dan outdoor.

## Fitur Utama
1. **Manajemen Alat**
   - CRUD data alat pendakian
   - Field: id, nama, kategori, stok, harga_per_hari, kondisi

2. **Manajemen Penyewa**
   - CRUD data penyewa
   - Field: id, nama, no_hp, alamat, jaminan

3. **Transaksi Penyewaan**
   - Admin dapat memilih penyewa
   - Admin dapat memilih lebih dari satu alat dalam satu transaksi
   - Input tanggal sewa dan tanggal rencana kembali
   - Sistem menghitung total biaya sewa otomatis
   - Stok alat otomatis berkurang setelah transaksi disimpan

4. **Pengembalian Alat**
   - Input tanggal kembali aktual
   - Hitung keterlambatan otomatis
   - Denda keterlambatan Rp10.000 per hari
   - Stok alat otomatis bertambah kembali
   - Status sewa berubah menjadi "Dikembalikan"

5. **Laporan**
   - Menampilkan daftar semua transaksi penyewaan
   - Menampilkan total pendapatan dan total denda
   - Laporan berdasarkan penyewa
   - Laporan berdasarkan alat

## Struktur Project
```
Sewa Alat Outdoor/
├── app.py                 # File utama Flask
├── models/               # Database models
│   ├── __init__.py
│   └── database.py       # Alat, Penyewa, Sewa, DetailSewa models
├── routes/              # Routes dan controllers
│   ├── __init__.py
│   ├── alat.py         # Routes untuk manajemen alat
│   ├── penyewa.py      # Routes untuk manajemen penyewa
│   ├── sewa.py         # Routes untuk transaksi sewa
│   └── laporan.py      # Routes untuk laporan
├── templates/          # Template HTML
│   ├── base.html       # Base template
│   ├── index.html      # Halaman beranda
│   ├── alat/
│   ├── penyewa/
│   ├── sewa/
│   └── laporan/
├── static/
│   └── css/
│       └── style.css   # CSS styling
├── sewa_alat.db       # Database SQLite (auto-generated)
└── requirements.txt   # Dependencies
```

## Requirement
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Bootstrap 5

## Instalasi

### 1. Install Dependencies
```bash
pip install flask flask-sqlalchemy
```

### 2. Jalankan Aplikasi
```bash
python app.py
```

### 3. Akses Aplikasi
Buka browser dan kunjungi: `http://localhost:5000`

## Database Models

### Model Alat
- id (Primary Key)
- nama (String, required)
- kategori (String, required)
- stok (Integer, default=0)
- harga_per_hari (Integer, required)
- kondisi (String, default='baik')
- created_at (DateTime)
- Relasi: DetailSewa (1:many)

### Model Penyewa
- id (Primary Key)
- nama (String, required)
- no_hp (String, required)
- alamat (Text, required)
- jaminan (String, required)
- created_at (DateTime)
- Relasi: Sewa (1:many)

### Model Sewa
- id (Primary Key)
- penyewa_id (Foreign Key to Penyewa)
- tanggal_sewa (DateTime, required)
- tanggal_rencana_kembali (DateTime, required)
- tanggal_kembali_aktual (DateTime, nullable)
- total_biaya (Integer, default=0)
- total_denda (Integer, default=0)
- status (String: 'aktif' | 'dikembalikan', default='aktif')
- created_at (DateTime)
- Relasi: Penyewa (many:1), DetailSewa (1:many)

### Model DetailSewa
- id (Primary Key)
- sewa_id (Foreign Key to Sewa)
- alat_id (Foreign Key to Alat)
- jumlah (Integer, default=1)
- harga_satuan (Integer, required)
- subtotal (Integer, default=0)

## Logika Bisnis

### Penyewaan
1. Admin memilih penyewa
2. Admin memilih satu atau lebih alat dengan jumlah masing-masing
3. Admin input tanggal sewa dan tanggal rencana kembali
4. Sistem menghitung jumlah hari
5. Sistem menghitung subtotal untuk setiap alat: harga_satuan × jumlah × jumlah_hari
6. Sistem menghitung total biaya
7. Stok alat berkurang sesuai jumlah yang disewa
8. Transaksi disimpan dengan status 'aktif'

### Pengembalian
1. Admin input tanggal kembali aktual
2. Sistem menghitung keterlambatan (jika tanggal kembali > tanggal rencana kembali)
3. Jika ada keterlambatan, denda = jumlah_hari_terlambat × Rp10.000
4. Stok alat bertambah kembali sesuai jumlah yang dikembalikan
5. Status sewa berubah menjadi 'dikembalikan'

## Fitur Keamanan
- No login required (Admin only)
- Form validation
- Error handling
- Database transaction safety
- CSRF protection ready (dapat ditambahkan dengan Flask-WTF)

## Catatan Penting
- Aplikasi ini untuk single admin (tanpa multi-user login)
- Database menggunakan SQLite (cocok untuk development dan small scale)
- Untuk production, gunakan PostgreSQL atau MySQL
- Tambahkan authentication jika akan diakses oleh multiple users

## Cara Menggunakan

### 1. Tambah Alat
- Navigasi ke "Manajemen Alat" → "+ Tambah Alat Baru"
- Isi form dengan data alat
- Klik "Tambah Alat"

### 2. Tambah Penyewa
- Navigasi ke "Manajemen Penyewa" → "+ Tambah Penyewa Baru"
- Isi form dengan data penyewa
- Klik "Tambah Penyewa"

### 3. Buat Transaksi Sewa
- Navigasi ke "Transaksi Sewa" → "+ Buat Transaksi Sewa Baru"
- Pilih penyewa
- Masukkan tanggal sewa dan rencana kembali
- Pilih alat dan jumlah (dapat menambah lebih dari satu alat)
- Klik "Buat Transaksi Sewa"

### 4. Proses Pengembalian
- Navigasi ke "Transaksi Sewa" → Klik "Detail"
- Klik "Proses Pengembalian"
- Masukkan tanggal kembali aktual
- Sistem otomatis hitung denda jika terlambat
- Klik "Proses Pengembalian"

### 5. Lihat Laporan
- Navigasi ke "Laporan"
- Lihat laporan umum, laporan penyewa, atau laporan alat

## Troubleshooting

### Database tidak buat
Pastikan folder project punya write permission, atau buat secara manual:
```python
from app import app
from models.database import db
with app.app_context():
    db.create_all()
```

### Port 5000 sudah digunakan
Ubah port di app.py:
```python
app.run(debug=True, host='localhost', port=5001)
```

## Pengembangan Lebih Lanjut
- Tambahkan fitur login/authentication
- Tambahkan email notification
- Tambahkan export laporan ke PDF/Excel
- Tambahkan SMS notification untuk keterlambatan
- Implementasikan pagination untuk tabel besar
- Tambahkan search dan filter functionality

---
Dibuat: 2026
Versi: 1.0
