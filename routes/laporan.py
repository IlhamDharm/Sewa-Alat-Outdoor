"""
Routes untuk Laporan
"""
from flask import Blueprint, render_template
from models.database import Sewa, DetailSewa
from sqlalchemy import func

laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')


@laporan_bp.route('/')
def index():
    """Tampilkan laporan umum"""
    # Total transaksi
    total_transaksi = Sewa.query.count()
    
    # Total pendapatan (dari transaksi yang sudah dikembalikan)
    total_pendapatan_query = Sewa.query.filter_by(status='dikembalikan').with_entities(
        func.sum(Sewa.total_biaya)
    ).scalar() or 0
    
    # Total denda
    total_denda_query = Sewa.query.with_entities(
        func.sum(Sewa.total_denda)
    ).scalar() or 0
    
    # Daftar semua sewa
    sewa_list = Sewa.query.all()
    
    return render_template('laporan/index.html',
                         total_transaksi=total_transaksi,
                         total_pendapatan=total_pendapatan_query,
                         total_denda=total_denda_query,
                         sewa_list=sewa_list)


@laporan_bp.route('/penyewa')
def laporan_penyewa():
    """Laporan berdasarkan penyewa"""
    from models.database import Penyewa
    
    penyewa_list = Penyewa.query.all()
    
    # Hitung total sewa per penyewa
    penyewa_stats = []
    for penyewa in penyewa_list:
        total_sewa = Sewa.query.filter_by(penyewa_id=penyewa.id).count()
        total_biaya = sum([s.total_biaya for s in Sewa.query.filter_by(penyewa_id=penyewa.id).all()])
        penyewa_stats.append({
            'penyewa': penyewa,
            'total_sewa': total_sewa,
            'total_biaya': total_biaya
        })
    
    return render_template('laporan/penyewa.html', penyewa_stats=penyewa_stats)


@laporan_bp.route('/alat')
def laporan_alat():
    """Laporan berdasarkan alat yang disewa"""
    from models.database import Alat
    
    alat_list = Alat.query.all()
    
    # Hitung total disewa per alat
    alat_stats = []
    for alat in alat_list:
        total_disewa = DetailSewa.query.filter_by(alat_id=alat.id).with_entities(
            func.sum(DetailSewa.jumlah)
        ).scalar() or 0
        
        total_pendapatan = DetailSewa.query.filter_by(alat_id=alat.id).with_entities(
            func.sum(DetailSewa.subtotal)
        ).scalar() or 0
        
        alat_stats.append({
            'alat': alat,
            'total_disewa': total_disewa,
            'total_pendapatan': total_pendapatan
        })
    
    return render_template('laporan/alat.html', alat_stats=alat_stats)
