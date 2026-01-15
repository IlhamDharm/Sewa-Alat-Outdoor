"""
RINGKASAN PROJECT STRUKTUR
Sistem Penyewaan Alat Pendakian & Outdoor
"""

PROJECT STRUCTURE TREE
======================

Sewa Alat Outdoor/
│
├─── 📄 app.py
│    └─ File utama Flask application
│       • Inisialisasi Flask app
│       • Konfigurasi database SQLite
│       • Register blueprints routes
│       • Route untuk home/dashboard
│       • Error handlers (404, 500)
│       • Custom template filter untuk currency
│
├─── 📄 init_db.py
│    └─ Script inisialisasi database dengan dummy data
│       • 10 data alat
│       • 5 data penyewa
│       • 2 transaksi sewa (example)
│
├─── 📄 requirements.txt
│    └─ Python dependencies list
│       • Flask==2.3.3
│       • Flask-SQLAlchemy==3.0.5
│       • SQLAlchemy==2.0.21
│
├─── 📄 README.md
│    └─ Dokumentasi lengkap project
│       • Deskripsi fitur
│       • Struktur database
│       • Cara instalasi
│       • Logika bisnis
│
├─── 📄 INSTALLATION.md
│    └─ Panduan instalasi & menjalankan aplikasi
│       • Prasyarat
│       • Langkah instalasi
│       • Troubleshooting
│       • Cara menggunakan
│
├─── 📄 API_ROUTES.md
│    └─ Dokumentasi API routes
│       • List semua endpoint
│       • Method HTTP
│       • Parameters
│       • Response format
│
├─── 📁 models/
│    │
│    ├─── 📄 __init__.py
│    │    └─ Package initialization
│    │
│    └─── 📄 database.py
│         └─ SQLAlchemy ORM Models
│            • Class Alat (Table: alat)
│            • Class Penyewa (Table: penyewa)
│            • Class Sewa (Table: sewa)
│            • Class DetailSewa (Table: detail_sewa)
│            • Relasi many-to-many & one-to-many
│
├─── 📁 routes/
│    │
│    ├─── 📄 __init__.py
│    │    └─ Package initialization
│    │
│    ├─── 📄 alat.py
│    │    └─ Blueprint: alat management
│    │       • GET /alat/           -> index
│    │       • GET /alat/tambah     -> form tambah
│    │       • POST /alat/tambah    -> simpan
│    │       • GET /alat/edit/<id>  -> form edit
│    │       • POST /alat/edit/<id> -> update
│    │       • POST /alat/hapus/<id> -> delete
│    │
│    ├─── 📄 penyewa.py
│    │    └─ Blueprint: penyewa management
│    │       • GET /penyewa/           -> index
│    │       • GET /penyewa/tambah     -> form tambah
│    │       • POST /penyewa/tambah    -> simpan
│    │       • GET /penyewa/edit/<id>  -> form edit
│    │       • POST /penyewa/edit/<id> -> update
│    │       • POST /penyewa/hapus/<id> -> delete
│    │
│    ├─── 📄 sewa.py
│    │    └─ Blueprint: sewa transaction management
│    │       • GET /sewa/                      -> index
│    │       • GET /sewa/tambah                -> form tambah
│    │       • POST /sewa/tambah               -> simpan (with logic)
│    │       • GET /sewa/detail/<id>           -> view detail
│    │       • GET /sewa/pengembalian/<id>     -> form pengembalian
│    │       • POST /sewa/pengembalian/<id>    -> proses pengembalian (with denda)
│    │       • POST /sewa/hapus/<id>           -> delete
│    │       • Helper: hitung_jumlah_hari()
│    │       • Helper: hitung_harga_detail()
│    │
│    └─── 📄 laporan.py
│         └─ Blueprint: reporting
│            • GET /laporan/         -> laporan umum
│            • GET /laporan/penyewa  -> laporan penyewa
│            • GET /laporan/alat     -> laporan alat
│
├─── 📁 templates/
│    │
│    ├─── 📄 base.html
│    │    └─ Base template (extends untuk semua page)
│    │       • Navbar dengan menu navigasi
│    │       • Flash messages area
│    │       • Bootstrap CSS & JS
│    │       • Custom CSS link
│    │       • Footer
│    │
│    ├─── 📄 index.html
│    │    └─ Home page / Dashboard
│    │       • Stats cards (total alat, penyewa, sewa)
│    │       • Quick links untuk navigasi
│    │
│    ├─── 📄 404.html
│    │    └─ Error page (Not Found)
│    │
│    ├─── 📄 500.html
│    │    └─ Error page (Server Error)
│    │
│    ├─── 📁 alat/
│    │    ├─── 📄 index.html    -> Daftar alat dengan tabel
│    │    └─── 📄 form.html     -> Form tambah/edit alat
│    │
│    ├─── 📁 penyewa/
│    │    ├─── 📄 index.html    -> Daftar penyewa dengan tabel
│    │    └─── 📄 form.html     -> Form tambah/edit penyewa
│    │
│    ├─── 📁 sewa/
│    │    ├─── 📄 index.html              -> Daftar transaksi sewa
│    │    ├─── 📄 form_tambah.html        -> Form buat sewa (dynamic alat selection)
│    │    ├─── 📄 detail.html             -> Detail transaksi sewa
│    │    └─── 📄 form_pengembalian.html  -> Form pengembalian (dengan hitung denda)
│    │
│    └─── 📁 laporan/
│         ├─── 📄 index.html    -> Laporan umum
│         ├─── 📄 penyewa.html  -> Laporan penyewa
│         └─── 📄 alat.html     -> Laporan alat
│
├─── 📁 static/
│    └─── 📁 css/
│         └─── 📄 style.css
│              └─ Custom Bootstrap styling
│                 • Navbar styling
│                 • Card styling
│                 • Button styling
│                 • Form styling
│                 • Table styling
│                 • Utility classes
│
└─── 📁 sewa_alat.db (auto-generated)
     └─ SQLite database file
        Tables:
        • alat
        • penyewa
        • sewa
        • detail_sewa


FLOW DIAGRAM
============

1. MANAJEMEN ALAT
   ┌─────────────────────────────────────────┐
   │ HALAMAN DAFTAR ALAT                     │
   │ - Tampilkan tabel semua alat             │
   │ - Tombol: Edit, Hapus, Tambah           │
   └─────────────────────────────────────────┘
         ↓                ↓                ↓
       Edit           Hapus           Tambah
         ↓                ↓                ↓
      FORM           CONFIRM          FORM
      EDIT           DELETE         TAMBAH

2. MANAJEMEN PENYEWA (sama seperti alat)

3. TRANSAKSI SEWA
   ┌──────────────────────────────────────────┐
   │ HALAMAN DAFTAR SEWA                      │
   │ - Tampilkan tabel transaksi (aktif/done) │
   │ - Tombol: Detail, Kembali, Hapus, Buat   │
   └──────────────────────────────────────────┘
         ↓            ↓          ↓        ↓
      Detail      Kembali     Hapus    Buat
         ↓            ↓          ↓        ↓
      DETAIL    FORM PEN.   CONFIRM   FORM BUAT
      SEWA      GEMBALIAN    DELETE    SEWA
               (HITUNG
               DENDA)


DATABASE SCHEMA
===============

TABLE: alat
├── id (Primary Key)
├── nama
├── kategori
├── stok
├── harga_per_hari
├── kondisi
└── created_at

TABLE: penyewa
├── id (Primary Key)
├── nama
├── no_hp
├── alamat
├── jaminan
└── created_at

TABLE: sewa
├── id (Primary Key)
├── penyewa_id (Foreign Key → penyewa)
├── tanggal_sewa
├── tanggal_rencana_kembali
├── tanggal_kembali_aktual (nullable)
├── total_biaya
├── total_denda
├── status (aktif / dikembalikan)
└── created_at

TABLE: detail_sewa
├── id (Primary Key)
├── sewa_id (Foreign Key → sewa)
├── alat_id (Foreign Key → alat)
├── jumlah
├── harga_satuan
└── subtotal


KEY FEATURES IMPLEMENTATION
===========================

✓ CRUD Alat
  - Validasi input
  - Flash messages
  - Error handling

✓ CRUD Penyewa
  - Validasi input
  - Flash messages
  - Error handling

✓ Transaksi Sewa (Complex Logic)
  - Pilih penyewa
  - Pilih multiple alat dengan jumlah
  - Validasi tanggal
  - Auto hitung jumlah hari
  - Auto hitung subtotal per alat
  - Auto hitung total biaya
  - Auto kurangi stok alat
  - Simpan sewa + detail_sewa

✓ Pengembalian Alat (Complex Logic)
  - Input tanggal kembali aktual
  - Auto hitung keterlambatan
  - Auto hitung denda (Rp10.000/hari)
  - Auto kembalikan stok alat
  - Update status sewa
  - Simpan total denda

✓ Laporan
  - Total transaksi
  - Total pendapatan
  - Total denda
  - Laporan per penyewa
  - Laporan per alat
  - Query aggregation (sum, count)


TECHNOLOGY STACK
================

Backend:
  • Python 3.8+
  • Flask 2.3.3
  • SQLAlchemy 2.0.21 (ORM)
  • Flask-SQLAlchemy 3.0.5

Frontend:
  • HTML5
  • CSS3 (Bootstrap 5)
  • JavaScript (Vanilla)
  • Jinja2 (Template Engine)

Database:
  • SQLite 3 (Development)

Deployment Ready For:
  • PostgreSQL
  • MySQL
  • Docker
  • Heroku / PythonAnywhere


TOTAL FILE COUNT
================

Python Files: 7
  ├─ app.py
  ├─ init_db.py
  ├─ models/__init__.py
  ├─ models/database.py
  ├─ routes/__init__.py
  ├─ routes/alat.py
  ├─ routes/penyewa.py
  ├─ routes/sewa.py
  └─ routes/laporan.py

HTML Templates: 12
  ├─ base.html
  ├─ index.html
  ├─ 404.html
  ├─ 500.html
  ├─ alat/index.html
  ├─ alat/form.html
  ├─ penyewa/index.html
  ├─ penyewa/form.html
  ├─ sewa/index.html
  ├─ sewa/form_tambah.html
  ├─ sewa/detail.html
  ├─ sewa/form_pengembalian.html
  ├─ laporan/index.html
  ├─ laporan/penyewa.html
  └─ laporan/alat.html

CSS Files: 1
  └─ static/css/style.css

Documentation: 4
  ├─ README.md
  ├─ INSTALLATION.md
  ├─ API_ROUTES.md
  └─ PROJECT_STRUCTURE.md (ini)

Config Files: 1
  └─ requirements.txt

Total: ~40 files (including folders)
Total Lines of Code: ~3000+ lines

---
Created: 2026
Version: 1.0
