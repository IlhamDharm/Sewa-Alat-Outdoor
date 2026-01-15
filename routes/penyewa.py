"""
Routes untuk manajemen Penyewa
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db, Penyewa

penyewa_bp = Blueprint('penyewa', __name__, url_prefix='/penyewa')


@penyewa_bp.route('/')
def index():
    """Tampilkan daftar semua penyewa"""
    penyewa_list = Penyewa.query.all()
    return render_template('penyewa/index.html', penyewa_list=penyewa_list)


@penyewa_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    """Tambah penyewa baru"""
    if request.method == 'POST':
        try:
            nama = request.form.get('nama')
            no_hp = request.form.get('no_hp')
            alamat = request.form.get('alamat')
            jaminan = request.form.get('jaminan')
            
            # Validasi input
            if not nama or not no_hp or not alamat or not jaminan:
                flash('Semua field harus diisi!', 'danger')
                return redirect(url_for('penyewa.tambah'))
            
            penyewa_baru = Penyewa(
                nama=nama,
                no_hp=no_hp,
                alamat=alamat,
                jaminan=jaminan
            )
            
            db.session.add(penyewa_baru)
            db.session.commit()
            flash(f'Penyewa "{nama}" berhasil ditambahkan!', 'success')
            return redirect(url_for('penyewa.index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('penyewa.tambah'))
    
    return render_template('penyewa/form.html', action='Tambah', penyewa=None)


@penyewa_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit data penyewa"""
    penyewa = Penyewa.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            penyewa.nama = request.form.get('nama')
            penyewa.no_hp = request.form.get('no_hp')
            penyewa.alamat = request.form.get('alamat')
            penyewa.jaminan = request.form.get('jaminan')
            
            if not penyewa.nama or not penyewa.no_hp or not penyewa.alamat or not penyewa.jaminan:
                flash('Semua field harus diisi!', 'danger')
                return redirect(url_for('penyewa.edit', id=id))
            
            db.session.commit()
            flash(f'Penyewa "{penyewa.nama}" berhasil diperbarui!', 'success')
            return redirect(url_for('penyewa.index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('penyewa.edit', id=id))
    
    return render_template('penyewa/form.html', action='Edit', penyewa=penyewa)


@penyewa_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    """Hapus penyewa"""
    penyewa = Penyewa.query.get_or_404(id)
    nama = penyewa.nama
    
    try:
        db.session.delete(penyewa)
        db.session.commit()
        flash(f'Penyewa "{nama}" berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('penyewa.index'))
