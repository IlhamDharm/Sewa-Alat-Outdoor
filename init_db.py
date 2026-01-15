"""
Script setup untuk inisialisasi database dengan data dummy
Jalankan: python init_db.py
"""

from app import app
from models.database import db, Alat, Penyewa, Sewa, DetailSewa
from datetime import datetime, timedelta

def init_database():
    """Inisialisasi database dengan data dummy"""
    
    with app.app_context():
        # Drop semua tabel (hanya untuk development)
        print("🗑️  Menghapus tabel lama...")
        db.drop_all()
        
        # Buat tabel baru
        print("📦 Membuat tabel baru...")
        db.create_all()
        
        # Tambah data Alat
        print("➕ Menambahkan data alat...")
        alat_list = [
            Alat(
                nama='Tenda Dome 2 Orang',
                kategori='Tenda',
                stok=5,
                harga_per_hari=50000,
                kondisi='baik'
            ),
            Alat(
                nama='Tenda Tunnel 4 Orang',
                kategori='Tenda',
                stok=3,
                harga_per_hari=75000,
                kondisi='baik'
            ),
            Alat(
                nama='Sleeping Bag Premium',
                kategori='Sleeping Bag',
                stok=10,
                harga_per_hari=25000,
                kondisi='baik'
            ),
            Alat(
                nama='Sleeping Bag Standard',
                kategori='Sleeping Bag',
                stok=8,
                harga_per_hari=15000,
                kondisi='baik'
            ),
            Alat(
                nama='Backpack 60L',
                kategori='Backpack',
                stok=6,
                harga_per_hari=30000,
                kondisi='baik'
            ),
            Alat(
                nama='Sepatu Hiking Merrell',
                kategori='Sepatu Hiking',
                stok=12,
                harga_per_hari=20000,
                kondisi='baik'
            ),
            Alat(
                nama='Helm Climbing',
                kategori='Perlengkapan Keselamatan',
                stok=8,
                harga_per_hari=15000,
                kondisi='baik'
            ),
            Alat(
                nama='Harness Climbing',
                kategori='Perlengkapan Keselamatan',
                stok=5,
                harga_per_hari=25000,
                kondisi='baik'
            ),
            Alat(
                nama='Kompor Camping Portable',
                kategori='Alat Memasak',
                stok=4,
                harga_per_hari=20000,
                kondisi='baik'
            ),
            Alat(
                nama='Panci Camping Set',
                kategori='Alat Memasak',
                stok=6,
                harga_per_hari=15000,
                kondisi='baik'
            ),
        ]
        db.session.add_all(alat_list)
        
        # Tambah data Penyewa
        print("➕ Menambahkan data penyewa...")
        penyewa_list = [
            Penyewa(
                nama='Budi Santoso',
                no_hp='081234567890',
                alamat='Jl. Merdeka No. 123, Jakarta Pusat',
                jaminan='KTP'
            ),
            Penyewa(
                nama='Siti Nurhaliza',
                no_hp='082345678901',
                alamat='Jl. Ahmad Yani No. 45, Bandung',
                jaminan='SIM'
            ),
            Penyewa(
                nama='Ahmad Hidayat',
                no_hp='083456789012',
                alamat='Jl. Sudirman No. 78, Yogyakarta',
                jaminan='Paspor'
            ),
            Penyewa(
                nama='Dewi Lestari',
                no_hp='084567890123',
                alamat='Jl. Gatot Subroto No. 56, Surabaya',
                jaminan='KTP'
            ),
            Penyewa(
                nama='Rinto Harahap',
                no_hp='085678901234',
                alamat='Jl. Merdeka Barat No. 34, Medan',
                jaminan='Kartu Pelajar'
            ),
        ]
        db.session.add_all(penyewa_list)
        
        # Commit alat dan penyewa untuk dapatkan ID
        db.session.commit()
        
        # Tambah data Sewa (transaksi)
        print("➕ Menambahkan data transaksi sewa...")
        
        # Transaksi 1
        tanggal_sewa = datetime.now() - timedelta(days=5)
        tanggal_rencana_kembali = datetime.now() - timedelta(days=2)
        
        sewa1 = Sewa(
            penyewa_id=1,
            tanggal_sewa=tanggal_sewa,
            tanggal_rencana_kembali=tanggal_rencana_kembali,
            tanggal_kembali_aktual=datetime.now() - timedelta(days=1),
            total_biaya=150000,
            total_denda=10000,
            status='dikembalikan'
        )
        db.session.add(sewa1)
        db.session.commit()
        
        # Detail Sewa 1
        detail1 = DetailSewa(
            sewa_id=sewa1.id,
            alat_id=1,
            jumlah=1,
            harga_satuan=50000,
            subtotal=150000
        )
        db.session.add(detail1)
        
        # Transaksi 2 (Aktif)
        tanggal_sewa2 = datetime.now() - timedelta(days=2)
        tanggal_rencana_kembali2 = datetime.now() + timedelta(days=2)
        
        sewa2 = Sewa(
            penyewa_id=2,
            tanggal_sewa=tanggal_sewa2,
            tanggal_rencana_kembali=tanggal_rencana_kembali2,
            total_biaya=200000,
            total_denda=0,
            status='aktif'
        )
        db.session.add(sewa2)
        db.session.commit()
        
        # Detail Sewa 2
        detail2_1 = DetailSewa(
            sewa_id=sewa2.id,
            alat_id=3,
            jumlah=2,
            harga_satuan=25000,
            subtotal=100000
        )
        detail2_2 = DetailSewa(
            sewa_id=sewa2.id,
            alat_id=5,
            jumlah=1,
            harga_satuan=30000,
            subtotal=100000
        )
        db.session.add(detail2_1)
        db.session.add(detail2_2)
        
        db.session.commit()
        
        # Update stok alat setelah sewa
        alat_1 = Alat.query.get(1)
        alat_1.stok -= 1  # Sudah dikembalikan di sewa1
        
        alat_3 = Alat.query.get(3)
        alat_3.stok -= 2  # Aktif di sewa2
        
        alat_5 = Alat.query.get(5)
        alat_5.stok -= 1  # Aktif di sewa2
        
        db.session.commit()
        
        print("✅ Database berhasil diinisialisasi dengan data dummy!")
        print("\n📊 Ringkasan Data:")
        print(f"   - Total Alat: {Alat.query.count()}")
        print(f"   - Total Penyewa: {Penyewa.query.count()}")
        print(f"   - Total Transaksi: {Sewa.query.count()}")
        print("\n🚀 Silakan jalankan 'python app.py' untuk memulai aplikasi")

if __name__ == '__main__':
    init_database()
