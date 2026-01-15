"""
Dokumentasi API Routes
Sistem Penyewaan Alat Pendakian & Outdoor
"""

# ========================
# MANAJEMEN ALAT ROUTES
# ========================

# GET: Tampilkan semua alat
# URL: /alat/
# Method: GET
# Response: HTML page dengan tabel daftar alat

# GET: Form tambah alat
# URL: /alat/tambah
# Method: GET
# Response: HTML form

# POST: Simpan alat baru
# URL: /alat/tambah
# Method: POST
# Parameters:
#   - nama (string, required)
#   - kategori (string, required)
#   - stok (integer, required)
#   - harga_per_hari (integer, required)
#   - kondisi (string, required)
# Response: Redirect ke /alat/ dengan flash message

# GET: Form edit alat
# URL: /alat/edit/<id>
# Method: GET
# Parameters:
#   - id (integer, path parameter)
# Response: HTML form dengan data alat

# POST: Update alat
# URL: /alat/edit/<id>
# Method: POST
# Parameters:
#   - nama (string, required)
#   - kategori (string, required)
#   - stok (integer, required)
#   - harga_per_hari (integer, required)
#   - kondisi (string, required)
# Response: Redirect ke /alat/ dengan flash message

# POST: Hapus alat
# URL: /alat/hapus/<id>
# Method: POST
# Parameters:
#   - id (integer, path parameter)
# Response: Redirect ke /alat/ dengan flash message


# ========================
# MANAJEMEN PENYEWA ROUTES
# ========================

# GET: Tampilkan semua penyewa
# URL: /penyewa/
# Method: GET
# Response: HTML page dengan tabel daftar penyewa

# GET: Form tambah penyewa
# URL: /penyewa/tambah
# Method: GET
# Response: HTML form

# POST: Simpan penyewa baru
# URL: /penyewa/tambah
# Method: POST
# Parameters:
#   - nama (string, required)
#   - no_hp (string, required)
#   - alamat (text, required)
#   - jaminan (string, required)
# Response: Redirect ke /penyewa/ dengan flash message

# GET: Form edit penyewa
# URL: /penyewa/edit/<id>
# Method: GET
# Parameters:
#   - id (integer, path parameter)
# Response: HTML form dengan data penyewa

# POST: Update penyewa
# URL: /penyewa/edit/<id>
# Method: POST
# Parameters:
#   - nama (string, required)
#   - no_hp (string, required)
#   - alamat (text, required)
#   - jaminan (string, required)
# Response: Redirect ke /penyewa/ dengan flash message

# POST: Hapus penyewa
# URL: /penyewa/hapus/<id>
# Method: POST
# Parameters:
#   - id (integer, path parameter)
# Response: Redirect ke /penyewa/ dengan flash message


# ========================
# TRANSAKSI SEWA ROUTES
# ========================

# GET: Tampilkan semua transaksi sewa
# URL: /sewa/
# Method: GET
# Response: HTML page dengan tabel daftar transaksi

# GET: Form buat sewa baru
# URL: /sewa/tambah
# Method: GET
# Response: HTML form dengan dropdown penyewa dan alat

# POST: Simpan transaksi sewa baru
# URL: /sewa/tambah
# Method: POST
# Parameters:
#   - penyewa_id (integer, required)
#   - tanggal_sewa (date, required)
#   - tanggal_rencana_kembali (date, required)
#   - alat_id[] (array of integers)
#   - alat_jumlah[] (array of integers)
# Logic:
#   1. Validasi tanggal
#   2. Hitung jumlah hari
#   3. Untuk setiap alat:
#      - Validasi stok tersedia
#      - Hitung subtotal: harga × jumlah × hari
#      - Kurangi stok
#   4. Hitung total biaya
#   5. Simpan sewa dan detail_sewa
# Response: Redirect ke /sewa/ dengan flash message

# GET: Lihat detail transaksi sewa
# URL: /sewa/detail/<id>
# Method: GET
# Parameters:
#   - id (integer, path parameter)
# Response: HTML page dengan detail sewa, daftar alat, dan ringkasan biaya

# GET: Form pengembalian alat
# URL: /sewa/pengembalian/<id>
# Method: GET
# Parameters:
#   - id (integer, path parameter)
# Response: HTML form untuk input tanggal kembali

# POST: Proses pengembalian alat
# URL: /sewa/pengembalian/<id>
# Method: POST
# Parameters:
#   - tanggal_kembali (date, required)
# Logic:
#   1. Hitung keterlambatan: tanggal_kembali - tanggal_rencana_kembali
#   2. Jika terlambat: denda = hari_terlambat × Rp10.000
#   3. Kembalikan stok alat
#   4. Update status sewa ke 'dikembalikan'
#   5. Update tanggal_kembali_aktual dan total_denda
# Response: Redirect ke /sewa/detail/<id> dengan flash message

# POST: Hapus transaksi sewa
# URL: /sewa/hapus/<id>
# Method: POST
# Parameters:
#   - id (integer, path parameter)
# Logic:
#   1. Cek status sewa (hanya bisa hapus jika 'aktif')
#   2. Kembalikan stok alat
#   3. Hapus transaksi dan detail_sewa
# Response: Redirect ke /sewa/ dengan flash message


# ========================
# LAPORAN ROUTES
# ========================

# GET: Laporan umum (dashboard laporan)
# URL: /laporan/
# Method: GET
# Response: HTML page dengan:
#   - Total transaksi
#   - Total pendapatan (sewa yang sudah dikembalikan)
#   - Total denda
#   - Tabel semua transaksi

# GET: Laporan berdasarkan penyewa
# URL: /laporan/penyewa
# Method: GET
# Response: HTML page dengan:
#   - Tabel penyewa
#   - Total sewa per penyewa
#   - Total biaya per penyewa

# GET: Laporan berdasarkan alat
# URL: /laporan/alat
# Method: GET
# Response: HTML page dengan:
#   - Tabel alat
#   - Total unit disewa
#   - Total pendapatan per alat


# ========================
# HOME ROUTES
# ========================

# GET: Halaman beranda (dashboard)
# URL: /
# Method: GET
# Response: HTML page dengan:
#   - Stats cards (total alat, penyewa, transaksi, aktif)
#   - Menu cepat untuk navigasi
