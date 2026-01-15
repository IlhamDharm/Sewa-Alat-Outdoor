"""
Routes untuk manajemen Sewa dan DetailSewa
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.database import db, Sewa, DetailSewa, Alat, Penyewa
from datetime import datetime, timedelta

sewa_bp = Blueprint('sewa', __name__, url_prefix='/sewa')


def hitung_jumlah_hari(tanggal_mulai, tanggal_akhir):
    """Hitung jumlah hari antara dua tanggal"""
    delta = tanggal_akhir - tanggal_mulai
    # Minimal 1 hari
    return max(1, delta.days)


def hitung_harga_detail(harga_satuan, jumlah, jumlah_hari):
    """Hitung subtotal untuk satu detail sewa"""
    return harga_satuan * jumlah * jumlah_hari


@sewa_bp.route('/')
def index():
    """Tampilkan daftar semua transaksi sewa"""
    sewa_list = Sewa.query.all()
    return render_template('sewa/index.html', sewa_list=sewa_list)


@sewa_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    """Buat transaksi sewa baru"""
    if request.method == 'POST':
        try:
            penyewa_id = int(request.form.get('penyewa_id'))
            tanggal_sewa_str = request.form.get('tanggal_sewa')
            tanggal_rencana_kembali_str = request.form.get('tanggal_rencana_kembali')
            
            # Parse tanggal
            tanggal_sewa = datetime.strptime(tanggal_sewa_str, '%Y-%m-%d')
            tanggal_rencana_kembali = datetime.strptime(tanggal_rencana_kembali_str, '%Y-%m-%d')
            
            # Validasi tanggal
            if tanggal_rencana_kembali <= tanggal_sewa:
                flash('Tanggal rencana kembali harus lebih besar dari tanggal sewa!', 'danger')
                return redirect(url_for('sewa.tambah'))
            
            # Cek penyewa ada atau tidak
            penyewa = Penyewa.query.get_or_404(penyewa_id)
            
            # Buat transaksi sewa baru
            sewa_baru = Sewa(
                penyewa_id=penyewa_id,
                tanggal_sewa=tanggal_sewa,
                tanggal_rencana_kembali=tanggal_rencana_kembali,
                status='aktif'
            )
            
            db.session.add(sewa_baru)
            db.session.flush()  # Dapatkan ID sewa
            
            # Proses detail sewa dari form
            total_biaya = 0
            jumlah_hari = hitung_jumlah_hari(tanggal_sewa, tanggal_rencana_kembali)
            
            # Ambil data alat dari form (dynamic fields)
            alat_ids = request.form.getlist('alat_id')
            alat_jumlah = request.form.getlist('alat_jumlah')
            
            if not alat_ids:
                db.session.rollback()
                flash('Minimal ada satu alat yang harus dipilih!', 'danger')
                return redirect(url_for('sewa.tambah'))
            
            # Loop untuk setiap alat yang dipilih
            for alat_id, jumlah in zip(alat_ids, alat_jumlah):
                if not alat_id or not jumlah:
                    continue
                
                alat_id = int(alat_id)
                jumlah = int(jumlah)
                
                # Cek alat ada atau tidak
                alat = Alat.query.get_or_404(alat_id)
                
                # Validasi stok
                if alat.stok < jumlah:
                    db.session.rollback()
                    flash(f'Stok {alat.nama} tidak cukup! Tersedia: {alat.stok}', 'danger')
                    return redirect(url_for('sewa.tambah'))
                
                # Hitung subtotal
                subtotal = hitung_harga_detail(alat.harga_per_hari, jumlah, jumlah_hari)
                
                # Buat detail sewa
                detail = DetailSewa(
                    sewa_id=sewa_baru.id,
                    alat_id=alat_id,
                    jumlah=jumlah,
                    harga_satuan=alat.harga_per_hari,
                    subtotal=subtotal
                )
                
                db.session.add(detail)
                
                # Kurangi stok alat
                alat.stok -= jumlah
                
                # Tambah total biaya
                total_biaya += subtotal
            
            # Update total biaya sewa
            sewa_baru.total_biaya = total_biaya
            
            db.session.commit()
            flash(f'Transaksi sewa berhasil dibuat! Total: Rp{total_biaya:,}', 'success')
            return redirect(url_for('sewa.index'))
        
        except ValueError as ve:
            db.session.rollback()
            flash(f'Format data tidak valid: {str(ve)}', 'danger')
            return redirect(url_for('sewa.tambah'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('sewa.tambah'))
    
    penyewa_list = Penyewa.query.all()
    alat_list = Alat.query.filter(Alat.stok > 0).all()
    return render_template('sewa/form_tambah.html', penyewa_list=penyewa_list, alat_list=alat_list)


@sewa_bp.route('/detail/<int:id>')
def detail(id):
    """Lihat detail transaksi sewa"""
    sewa = Sewa.query.get_or_404(id)
    detail_sewa = DetailSewa.query.filter_by(sewa_id=id).all()
    
    return render_template('sewa/detail.html', sewa=sewa, detail_sewa=detail_sewa)


@sewa_bp.route('/pengembalian/<int:id>', methods=['GET', 'POST'])
def pengembalian(id):
    """Proses pengembalian alat"""
    sewa = Sewa.query.get_or_404(id)
    
    # Cek apakah transaksi sudah dikembalikan
    if sewa.status == 'dikembalikan':
        flash('Transaksi ini sudah dikembalikan!', 'warning')
        return redirect(url_for('sewa.detail', id=id))
    
    if request.method == 'POST':
        try:
            tanggal_kembali_str = request.form.get('tanggal_kembali')
            tanggal_kembali = datetime.strptime(tanggal_kembali_str, '%Y-%m-%d')
            
            # Hitung keterlambatan
            hari_keterlambatan = (tanggal_kembali - sewa.tanggal_rencana_kembali).days
            
            # Jika ada keterlambatan, hitung denda (Rp10.000 per hari)
            if hari_keterlambatan > 0:
                denda_per_hari = 10000
                total_denda = hari_keterlambatan * denda_per_hari
                sewa.total_denda = total_denda
            
            # Update status dan tanggal kembali aktual
            sewa.tanggal_kembali_aktual = tanggal_kembali
            sewa.status = 'dikembalikan'
            
            # Kembalikan stok alat
            detail_list = DetailSewa.query.filter_by(sewa_id=id).all()
            for detail in detail_list:
                detail.alat.stok += detail.jumlah
            
            db.session.commit()
            
            pesan = f'Pengembalian berhasil diproses!'
            if hari_keterlambatan > 0:
                pesan += f' Denda keterlambatan {hari_keterlambatan} hari: Rp{sewa.total_denda:,}'
            
            flash(pesan, 'success')
            return redirect(url_for('sewa.detail', id=id))
        
        except ValueError:
            flash('Format tanggal tidak valid!', 'danger')
            return redirect(url_for('sewa.pengembalian', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('sewa.pengembalian', id=id))
    
    return render_template('sewa/form_pengembalian.html', sewa=sewa)


@sewa_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    """Hapus transaksi sewa (hanya untuk yang belum dikembalikan)"""
    sewa = Sewa.query.get_or_404(id)
    
    # Hanya bisa menghapus jika masih aktif
    if sewa.status == 'dikembalikan':
        flash('Tidak bisa menghapus transaksi yang sudah dikembalikan!', 'warning')
        return redirect(url_for('sewa.index'))
    
    try:
        # Kembalikan stok alat
        detail_list = DetailSewa.query.filter_by(sewa_id=id).all()
        for detail in detail_list:
            detail.alat.stok += detail.jumlah
        
        # Hapus transaksi
        db.session.delete(sewa)
        db.session.commit()
        flash('Transaksi sewa berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('sewa.index'))
