"""
TESTING GUIDE & CHECKLIST
Sistem Penyewaan Alat Outdoor
"""

═════════════════════════════════════════════════════════════════════════════
                         TESTING CHECKLIST
═════════════════════════════════════════════════════════════════════════════


SETUP TESTING
═════════════════════════════════════════════════════════════════════════════

1. Install dependencies:
   pip install -r requirements.txt

2. Initialize database dengan dummy data:
   python init_db.py

   Data yang dibuat:
   - 10 alat (berbagai kategori)
   - 5 penyewa
   - 2 transaksi sewa (1 aktif, 1 sudah dikembalikan)

3. Jalankan aplikasi:
   python app.py

4. Akses browser:
   http://localhost:5000


FEATURE TESTING
═════════════════════════════════════════════════════════════════════════════

FITUR 1: DASHBOARD / HOME PAGE
☐ Tampilkan halaman home dengan 4 stat cards
☐ Stat cards menampilkan:
  ☐ Total alat (harus 10 dari dummy data)
  ☐ Total penyewa (harus 5)
  ☐ Total transaksi aktif (harus 1)
  ☐ Total transaksi (harus 2)
☐ Navbar menampilkan 4 menu utama
☐ Quick links menampilkan dengan benar
☐ Footer ter-render di bawah


FITUR 2: MANAJEMEN ALAT
─────────────────────────────────────────────────────────────────────────────

Test CRUD Alat:

CREATE (Tambah Alat):
☐ Klik "Manajemen Alat" di navbar
☐ Klik "+ Tambah Alat Baru"
☐ Form terbuka dengan field kosong
☐ Isi form dengan data valid:
  ☐ Nama: "Test Alat ABC"
  ☐ Kategori: Pilih dari dropdown
  ☐ Stok: 5
  ☐ Harga/Hari: 50000
  ☐ Kondisi: "baik"
☐ Klik "Tambah Alat"
☐ Redirect ke daftar alat
☐ Flash message tampil: "Alat "Test Alat ABC" berhasil ditambahkan!"
☐ Alat baru muncul di tabel (11 alat)

Validasi Input (Tambah Alat):
☐ Coba submit form kosong → Error: "Nama dan kategori alat harus diisi!"
☐ Coba input stok non-numeric → Error: "Stok dan harga harus berupa angka!"

READ (Lihat Alat):
☐ Daftar alat ter-render dengan tabel
☐ Tabel menampilkan columns:
  ☐ No
  ☐ Nama Alat
  ☐ Kategori
  ☐ Stok (dengan badge)
  ☐ Harga/Hari
  ☐ Kondisi (dengan badge color)
  ☐ Aksi (Edit, Hapus)
☐ Stok badge warna:
  ☐ Green jika > 5
  ☐ Yellow jika 1-5
  ☐ Red jika 0
☐ Kondisi badge:
  ☐ Green untuk "baik"
  ☐ Yellow untuk "rusak"
  ☐ Red untuk "rusak berat"

UPDATE (Edit Alat):
☐ Klik button "Edit" di salah satu alat
☐ Form terbuka dengan data yang sudah ada
☐ Ubah data (contoh: Stok dari 11 → 15)
☐ Klik "Edit Alat"
☐ Redirect ke daftar alat
☐ Flash message: "Alat berhasil diperbarui!"
☐ Perubahan ter-apply di tabel

DELETE (Hapus Alat):
☐ Klik button "Hapus" pada alat
☐ Modal confirmation muncul
☐ Klik "Batal" → Modal ditutup, data tidak dihapus
☐ Klik "Hapus" lagi → Modal muncul
☐ Klik "Hapus" di modal → Data dihapus
☐ Flash message: "Alat berhasil dihapus!"
☐ Tabel updated (kembali ke 10 alat)


FITUR 3: MANAJEMEN PENYEWA
─────────────────────────────────────────────────────────────────────────────

Test CRUD Penyewa (sama seperti Alat):

CREATE:
☐ Klik "Manajemen Penyewa" → "+ Tambah Penyewa Baru"
☐ Isi form:
  ☐ Nama: "Test Penyewa XYZ"
  ☐ No HP: "081234567890"
  ☐ Alamat: "Jl. Test No. 123"
  ☐ Jaminan: "KTP"
☐ Klik "Tambah Penyewa"
☐ Success message & data muncul di tabel (6 penyewa)

Validasi:
☐ Submit form kosong → Error: "Semua field harus diisi!"

READ:
☐ Tabel penyewa ter-render dengan benar
☐ Columns: No, Nama, No HP, Alamat, Jaminan, Aksi

UPDATE:
☐ Edit salah satu penyewa
☐ Ubah data
☐ Save & verify perubahan

DELETE:
☐ Hapus dengan modal confirmation
☐ Verify data terhapus (kembali ke 5 penyewa)


FITUR 4: TRANSAKSI PENYEWAAN (CORE FEATURE)
─────────────────────────────────────────────────────────────────────────────

Test Buat Sewa Baru:

CREATE (Buat Sewa):
☐ Klik "Transaksi Sewa" → "+ Buat Transaksi Sewa Baru"
☐ Form terbuka dengan:
  ☐ Dropdown penyewa (semua 5 penyewa ada)
  ☐ Input tanggal sewa (default = hari ini)
  ☐ Input tanggal rencana kembali
  ☐ 1 alat item dengan dropdown alat & input jumlah
  ☐ Button "+ Tambah Alat Lain"

Isi Form Test Case 1 (1 alat, 3 hari):
☐ Penyewa: "Budi Santoso"
☐ Tgl Sewa: 2026-01-15
☐ Tgl Rencana Kembali: 2026-01-18 (3 hari)
☐ Alat: "Tenda Dome 2 Orang" (harga 50000/hari)
☐ Jumlah: 1

Kalkulasi yang harus terjadi:
☐ Hari = 18-15 = 3 hari
☐ Subtotal = 50000 × 1 × 3 = 150000
☐ Total = 150000

☐ Klik "Buat Transaksi Sewa"
☐ Success message & redirect ke daftar sewa
☐ Transaksi baru muncul di tabel (3 transaksi)
☐ Status: "Aktif" (badge green)

Verify Stok Berkurang:
☐ Pergi ke "Manajemen Alat"
☐ Cek stok "Tenda Dome 2 Orang"
☐ Stok sebelumnya: 5 (dari dummy data)
☐ Stok sekarang: 4 ✓ (berkurang 1)

Test Case 2 (Multiple alat):
☐ Buat sewa baru dengan 2 alat
☐ Alat 1: "Sleeping Bag Premium" qty 2
☐ Alat 2: "Backpack 60L" qty 1
☐ Tanggal: 2026-01-15 s/d 2026-01-17 (2 hari)

Kalkulasi:
☐ Alat 1: 25000 × 2 × 2 = 100000
☐ Alat 2: 30000 × 1 × 2 = 60000
☐ Total: 160000

☐ Submit & verify total biaya
☐ Cek stok:
  ☐ Sleeping Bag (10 → 8) ✓
  ☐ Backpack (6 → 5) ✓

Validasi Tanggal:
☐ Coba: Tgl Sewa > Tgl Rencana Kembali
☐ Error: "Tanggal rencana kembali harus lebih besar!"

Validasi Stok:
☐ Coba sewa alat dengan qty > stok
☐ Error: "Stok [nama alat] tidak cukup! Tersedia: [stok]"

Validasi Alat:
☐ Coba submit tanpa pilih alat
☐ Error: "Minimal ada satu alat yang harus dipilih!"

READ (Lihat Transaksi):
☐ Daftar sewa ter-render dengan tabel
☐ Columns: No, ID, Penyewa, Tgl Sewa, Tgl Rencana, Total, Status, Aksi
☐ Status badge warna:
  ☐ Green untuk "Aktif"
  ☐ Gray untuk "Dikembalikan"

Detail Sewa:
☐ Klik "Detail" pada sewa aktif
☐ Detail page menampilkan:
  ☐ Info penyewa (nama, HP, alamat, jaminan)
  ☐ Info sewa (tanggal, status)
  ☐ Tabel alat yang disewa (nama, qty, harga, subtotal)
  ☐ Ringkasan pembayaran (total biaya, denda, total)
  ☐ Button "Proses Pengembalian" (aktif)
  ☐ Button "Hapus Transaksi"

DELETE (Hapus Sewa):
☐ Dari detail sewa, klik "Hapus Transaksi"
☐ Modal confirmation muncul
☐ Klik "Hapus"
☐ Transaksi dihapus
☐ Stok alat kembali (restored)
☐ Flash: "Transaksi sewa berhasil dihapus!"

Prevent Delete (Sudah Dikembalikan):
☐ Jangan bisa hapus transaksi dengan status "Dikembalikan"
☐ Warning message: "Tidak bisa menghapus transaksi yang sudah dikembalikan!"


FITUR 5: PENGEMBALIAN ALAT (COMPLEX LOGIC)
─────────────────────────────────────────────────────────────────────────────

Test Pengembalian Tepat Waktu:

☐ Buat sewa baru:
  - Tgl Sewa: 2026-01-15
  - Tgl Rencana Kembali: 2026-01-17
  - Alat: Tenda (harga 50000/hari)
  - Total: 100000 (2 hari)

☐ Stok berkurang (verified)

☐ Klik "Detail" → "Proses Pengembalian"
☐ Form pengembalian tampil
☐ Input Tgl Pengembalian: 2026-01-17 (tepat waktu)
☐ Alert "⚠️ Perhatian" TIDAK muncul (karena tidak terlambat)
☐ Klik "Proses Pengembalian"
☐ Success message
☐ Denda = 0
☐ Total pembayaran = 100000 (biaya saja)
☐ Status berubah menjadi "Dikembalikan"

Verify Stok Bertambah:
☐ Lihat stok tenda
☐ Stok kembali ke nilai semula ✓

Test Pengembalian Terlambat:

☐ Buat sewa baru:
  - Tgl Sewa: 2026-01-15
  - Tgl Rencana Kembali: 2026-01-17
  - Alat: Sleeping Bag (harga 25000/hari)
  - Total: 50000 (2 hari)

☐ Klik "Detail" → "Proses Pengembalian"
☐ Input Tgl Pengembalian: 2026-01-20 (3 hari terlambat)

Kalkulasi Denda:
☐ Terlambat = 20 - 17 = 3 hari
☐ Denda = 3 × 10000 = 30000

☐ Alert "⚠️ Perhatian" muncul dengan:
  ☐ "Terdapat keterlambatan 3 hari"
  ☐ "Denda: Rp30,000"

☐ Klik "Proses Pengembalian"
☐ Success message menampilkan denda
☐ Total Denda di detail sewa: 30000 ✓
☐ Total pembayaran: 50000 + 30000 = 80000 ✓
☐ Status: "Dikembalikan"
☐ Stok kembali ✓

Test Denda Calculation berbagai hari:
☐ 1 hari terlambat → Rp10,000
☐ 5 hari terlambat → Rp50,000
☐ 10 hari terlambat → Rp100,000


FITUR 6: LAPORAN
─────────────────────────────────────────────────────────────────────────────

Test Laporan Umum:
☐ Klik "Laporan"
☐ 4 stat cards menampilkan:
  ☐ Total Transaksi: [total]
  ☐ Total Pendapatan: sum(biaya sewa yang dikembalikan)
  ☐ Total Denda: sum(denda)
  ☐ Total Penerimaan: pendapatan + denda

☐ Tabel transaksi menampilkan:
  - ID, Penyewa, Tgl, Total Biaya, Denda, Total, Status

Contoh dari dummy data:
  - Transaksi 1 (dikembalikan): Biaya 150000, Denda 10000
  - Transaksi 2 (aktif): Biaya 200000, Denda 0
  - Expected:
    ☐ Total Transaksi: 2+
    ☐ Total Pendapatan: 150000
    ☐ Total Denda: 10000
    ☐ Total Penerimaan: 160000

Test Laporan Penyewa:
☐ Klik "Laporan Penyewa"
☐ Tabel menampilkan:
  - Nama Penyewa, No HP, Total Sewa, Total Biaya
☐ Count total sewa per penyewa correct
☐ Sum total biaya per penyewa correct

Test Laporan Alat:
☐ Klik "Laporan Alat"
☐ Tabel menampilkan:
  - Nama Alat, Kategori, Stok, Total Disewa, Total Pendapatan
☐ Count total unit disewa per alat correct
☐ Sum pendapatan per alat correct


UI/UX TESTING
═════════════════════════════════════════════════════════════════════════════

Navigation:
☐ Navbar links bekerja dengan baik
☐ Active link di-highlight
☐ Menu responsif di mobile
☐ Dropdown penyewa/alat populated
☐ Form fields accessible

Styling:
☐ Bootstrap 5 styling applied
☐ Color scheme consistent
☐ Tables readable
☐ Buttons visible & clickable
☐ Flash messages styled properly
☐ Modals centered & styled
☐ Responsive di berbagai ukuran layar

Form Behavior:
☐ Required fields di-indicate dengan *
☐ Input type correct (date, number, text)
☐ Placeholder text helpful
☐ Error messages clear
☐ Success messages clear

Data Validation:
☐ String field: max length
☐ Number field: only numbers
☐ Date field: valid format
☐ Required field: cannot empty
☐ Foreign key: must exist


ERROR HANDLING TESTING
═════════════════════════════════════════════════════════════════════════════

Graceful Error Handling:
☐ Non-existent ID → 404 page dengan link kembali
☐ Database error → 500 page dengan link kembali
☐ Form validation error → Flash message & stay on page
☐ Missing parameters → Error handling active

Database Rollback:
☐ Buat sewa, stok berkurang
☐ Error saat save → Stok dikembalikan
☐ Verify: Stok tidak hilang setelah error


PERFORMANCE TESTING
═════════════════════════════════════════════════════════════════════════════

Response Time:
☐ Home page load < 1 detik
☐ List page load < 1 detik
☐ Form page load < 1 detik
☐ Save/update < 1 detik

Database:
☐ Tidak ada N+1 query problems
☐ Foreign key constraints work
☐ Cascade delete works (alat hapus → detail_sewa ikut hapus)

Load Testing (Optional):
☐ Buat 100+ transaksi
☐ Laporan masih responsive
☐ Query time acceptable


EDGE CASE TESTING
═════════════════════════════════════════════════════════════════════════════

☐ Sewa alat dengan stok 0 → Rejected
☐ Denda calculation dengan 30+ hari → Correct
☐ Ubah harga alat → Tidak mempengaruhi transaksi lama (harga tersimpan)
☐ Hapus alat yang sedang disewa → Cascade delete atau error
☐ Ubah stok alat manual → Tidak crash
☐ Sewa dengan multiple alat yang sama → Handled correctly
☐ Pengembalian sama hari sewa → Dihitung 1 hari (not 0)


REGRESSION TESTING
═════════════════════════════════════════════════════════════════════════════

Setelah setiap perubahan, test:
☐ CRUD Alat masih berfungsi
☐ CRUD Penyewa masih berfungsi
☐ Sewa creation & stok deduction
☐ Pengembalian & denda calculation
☐ Laporan menampilkan data correct
☐ Navigation & menu
☐ Flash messages


FINAL SIGN-OFF CHECKLIST
═════════════════════════════════════════════════════════════════════════════

Core Functionality:
☐ CRUD Alat: Create, Read, Update, Delete ✓
☐ CRUD Penyewa: Create, Read, Update, Delete ✓
☐ Sewa Creation dengan auto-calculation ✓
☐ Pengembalian dengan denda ✓
☐ Stok management (decrease & increase) ✓
☐ Laporan (3 jenis) ✓

Data Integrity:
☐ Relasi foreign key work ✓
☐ Cascade delete work ✓
☐ Transaction safety ✓

User Experience:
☐ UI professional & responsive ✓
☐ Navigation intuitive ✓
☐ Error messages clear ✓
☐ Success feedback visible ✓

Documentation:
☐ README.md lengkap ✓
☐ INSTALLATION.md ada ✓
☐ API_ROUTES.md lengkap ✓
☐ Code comments sufficient ✓


═════════════════════════════════════════════════════════════════════════════

HASIL TEST SUMMARY:
Total Test Cases: 100+
Expected Result: PASSED ✓

Jika semua test cases PASSED, aplikasi READY FOR PRODUCTION (dengan minor tweaks)

═════════════════════════════════════════════════════════════════════════════

Date Tested: _______________
Tester Name: _______________
Status:     ☐ PASSED    ☐ FAILED    ☐ NEEDS REVIEW
Comments:   ___________________________________________________

═════════════════════════════════════════════════════════════════════════════
