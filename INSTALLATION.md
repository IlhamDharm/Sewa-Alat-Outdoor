"""
Panduan Instalasi dan Menjalankan Aplikasi
Sistem Penyewaan Alat Pendakian & Outdoor
"""

# ==========================================
# PRASYARAT
# ==========================================

Sebelum menjalankan aplikasi, pastikan Anda memiliki:
1. Python 3.8 atau lebih tinggi
2. pip (Python Package Manager)
3. Git (opsional, untuk clone repo)

# ==========================================
# LANGKAH INSTALASI
# ==========================================

## 1. Buka Command Prompt / Terminal

Windows: Tekan Windows + R, ketik 'cmd', tekan Enter
Mac/Linux: Buka Terminal aplikasi

## 2. Navigate ke folder project

```
cd "c:\laragon\www\Sewa Alat Outdoor"
```

## 3. Buat Virtual Environment (Opsional tapi Disarankan)

```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Dependencies

```
pip install -r requirements.txt
```

Atau install manual:
```
pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install SQLAlchemy==2.0.21
```

## 5. Inisialisasi Database (Opsional)

Untuk mengisi database dengan data dummy:

```
python init_db.py
```

Ini akan membuat:
- 10 data alat
- 5 data penyewa
- 2 transaksi sewa (1 sudah dikembalikan, 1 aktif)

Jika tidak menjalankan ini, database akan otomatis dibuat kosong 
ketika Anda menjalankan aplikasi pertama kali.

## 6. Jalankan Aplikasi

```
python app.py
```

Anda akan melihat output seperti:
```
==================================================
Sistem Penyewaan Alat Pendakian & Outdoor
==================================================
Server running on http://localhost:5000
Press CTRL+C to stop the server
==================================================
```

## 7. Akses Aplikasi

Buka browser dan kunjungi:
```
http://localhost:5000
```

Anda akan melihat halaman Dashboard dengan menu navigasi.

# ==========================================
# STRUKTUR FOLDER
# ==========================================

Sewa Alat Outdoor/
├── app.py                    # File utama aplikasi Flask
├── init_db.py               # Script inisialisasi database dengan dummy data
├── requirements.txt         # List dependencies Python
├── README.md                # Dokumentasi project
├── API_ROUTES.md            # Dokumentasi API routes
├── INSTALLATION.md          # File ini
│
├── models/
│   ├── __init__.py
│   └── database.py          # Database models (Alat, Penyewa, Sewa, DetailSewa)
│
├── routes/
│   ├── __init__.py
│   ├── alat.py             # Routes untuk manajemen alat
│   ├── penyewa.py          # Routes untuk manajemen penyewa
│   ├── sewa.py             # Routes untuk transaksi sewa
│   └── laporan.py          # Routes untuk laporan
│
├── templates/
│   ├── base.html           # Base template (navbar, footer, flash messages)
│   ├── index.html          # Halaman beranda/dashboard
│   ├── 404.html            # Error page (not found)
│   ├── 500.html            # Error page (server error)
│   │
│   ├── alat/
│   │   ├── index.html      # Daftar alat
│   │   └── form.html       # Form tambah/edit alat
│   │
│   ├── penyewa/
│   │   ├── index.html      # Daftar penyewa
│   │   └── form.html       # Form tambah/edit penyewa
│   │
│   ├── sewa/
│   │   ├── index.html              # Daftar transaksi sewa
│   │   ├── form_tambah.html        # Form buat sewa baru
│   │   ├── detail.html             # Detail sewa
│   │   └── form_pengembalian.html  # Form pengembalian alat
│   │
│   └── laporan/
│       ├── index.html      # Laporan umum
│       ├── penyewa.html    # Laporan penyewa
│       └── alat.html       # Laporan alat
│
├── static/
│   └── css/
│       └── style.css       # CSS styling (Bootstrap custom)
│
└── sewa_alat.db           # Database SQLite (auto-generated)

# ==========================================
# TROUBLESHOOTING
# ==========================================

## Error: 'python' is not recognized

Gunakan 'python3' atau gunakan full path ke Python executable.

## Error: ModuleNotFoundError: No module named 'flask'

Pastikan virtual environment sudah aktif dan dependencies sudah install:
```
pip install -r requirements.txt
```

## Error: Port 5000 sudah digunakan

Edit app.py baris terakhir:
```python
app.run(debug=True, host='localhost', port=5001)  # Ubah port ke 5001
```

## Database tidak buat

Pastikan folder project punya write permission. Jika masih error, 
buat database secara manual:

Buat file 'setup_db.py':
```python
from app import app
from models.database import db

with app.app_context():
    db.create_all()
    print("Database created!")
```

Jalankan:
```
python setup_db.py
```

## Error: Address already in use

Cari process yang menggunakan port 5000:

Windows:
```
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Mac/Linux:
```
lsof -i :5000
kill -9 <PID>
```

# ==========================================
# MENGGUNAKAN APLIKASI
# ==========================================

## 1. Tambah Alat Baru

1. Klik "Manajemen Alat" di navbar
2. Klik "+ Tambah Alat Baru"
3. Isi form:
   - Nama Alat: Nama yang jelas (contoh: "Tenda Dome 2 Orang")
   - Kategori: Pilih dari dropdown
   - Stok: Berapa banyak alat tersedia
   - Harga/Hari: Harga sewa per hari dalam Rupiah
   - Kondisi: Pilih Baik/Rusak/Rusak Berat
4. Klik "Tambah Alat"

## 2. Tambah Penyewa Baru

1. Klik "Manajemen Penyewa" di navbar
2. Klik "+ Tambah Penyewa Baru"
3. Isi form:
   - Nama Penyewa: Nama lengkap
   - No HP: Nomor telepon
   - Alamat: Alamat lengkap
   - Jaminan: Tipe jaminan (KTP/SIM/Paspor/dll)
4. Klik "Tambah Penyewa"

## 3. Buat Transaksi Sewa Baru

1. Klik "Transaksi Sewa" di navbar
2. Klik "+ Buat Transaksi Sewa Baru"
3. Isi form:
   - Penyewa: Pilih dari dropdown
   - Tgl Sewa: Tanggal sewa dimulai
   - Tgl Rencana Kembali: Kapan alat akan dikembalikan
   - Alat: Pilih alat dan jumlah
   - Klik "+ Tambah Alat Lain" untuk menambah alat lain
4. Sistem otomatis hitung:
   - Jumlah hari sewa
   - Subtotal per alat (harga × jumlah × hari)
   - Total biaya sewa
5. Klik "Buat Transaksi Sewa"

Stok alat akan otomatis berkurang.

## 4. Proses Pengembalian Alat

1. Klik "Transaksi Sewa" di navbar
2. Cari transaksi yang ingin dikembalikan (status: Aktif)
3. Klik "Detail"
4. Klik "Proses Pengembalian"
5. Masukkan tanggal pengembalian aktual
6. Sistem otomatis hitung:
   - Keterlambatan (jika ada)
   - Denda (Rp10.000 per hari terlambat)
7. Klik "Proses Pengembalian"

Stok alat akan otomatis bertambah kembali.

## 5. Lihat Laporan

1. Klik "Laporan" di navbar
2. Pilih tipe laporan:
   - Laporan Umum: Total transaksi, pendapatan, denda
   - Laporan Penyewa: Statistik per penyewa
   - Laporan Alat: Statistik per alat

# ==========================================
# FITUR KEAMANAN
# ==========================================

Aplikasi ini adalah single-admin application tanpa login.
Jika ingin menambahkan login, Anda dapat menggunakan:

1. Flask-Login untuk session management
2. Werkzeug untuk password hashing
3. Flask-WTF untuk CSRF protection

Contoh untuk upgrade di masa depan.

# ==========================================
# TIPS & TRIK
# ==========================================

1. Gunakan data dummy (init_db.py) untuk testing
2. Backup database secara berkala
3. Untuk production, gunakan PostgreSQL atau MySQL
4. Tambahkan email notification untuk transaksi
5. Implementasikan search dan filter untuk tabel besar
6. Export laporan ke PDF untuk archiving

# ==========================================
# MENDAPATKAN BANTUAN
# ==========================================

Jika mengalami masalah:
1. Baca README.md untuk dokumentasi lengkap
2. Periksa API_ROUTES.md untuk daftar routes
3. Lihat komentar dalam kode untuk penjelasan logic
4. Cek error message di browser atau console

# ==========================================
# CATATAN PENTING
# ==========================================

- Aplikasi berjalan di localhost:5000 secara default
- Database menggunakan SQLite (cocok untuk development)
- Jangan gunakan debug=True untuk production
- Ganti SECRET_KEY di app.py untuk production
- Tambahkan authentication jika untuk multiple users

---
Selamat menggunakan Sistem Penyewaan Alat Outdoor!
