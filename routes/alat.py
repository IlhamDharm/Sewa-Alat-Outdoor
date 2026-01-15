"""
Routes untuk manajemen Alat
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db, Alat

alat_bp = Blueprint('alat', __name__, url_prefix='/alat')


@alat_bp.route('/')
def index():
    """Tampilkan daftar semua alat"""
    alat_list = Alat.query.all()
    return render_template('alat/index.html', alat_list=alat_list)


@alat_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    """Tambah alat baru"""
    if request.method == 'POST':
        try:
            nama = request.form.get('nama')
            kategori = request.form.get('kategori')
            stok = int(request.form.get('stok', 0))
            harga_per_hari = int(request.form.get('harga_per_hari', 0))
            kondisi = request.form.get('kondisi', 'baik')
            
            # Validasi input
            if not nama or not kategori:
                flash('Nama dan kategori alat harus diisi!', 'danger')
                return redirect(url_for('alat.tambah'))
            
            alat_baru = Alat(
                nama=nama,
                kategori=kategori,
                stok=stok,
                harga_per_hari=harga_per_hari,
                kondisi=kondisi
            )
            
            db.session.add(alat_baru)
            db.session.commit()
            flash(f'Alat "{nama}" berhasil ditambahkan!', 'success')
            return redirect(url_for('alat.index'))
        
        except ValueError:
            flash('Stok dan harga harus berupa angka!', 'danger')
            return redirect(url_for('alat.tambah'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('alat.tambah'))
    
    return render_template('alat/form.html', action='Tambah', alat=None)


@alat_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit data alat"""
    alat = Alat.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            alat.nama = request.form.get('nama')
            alat.kategori = request.form.get('kategori')
            alat.stok = int(request.form.get('stok', 0))
            alat.harga_per_hari = int(request.form.get('harga_per_hari', 0))
            alat.kondisi = request.form.get('kondisi', 'baik')
            
            if not alat.nama or not alat.kategori:
                flash('Nama dan kategori alat harus diisi!', 'danger')
                return redirect(url_for('alat.edit', id=id))
            
            db.session.commit()
            flash(f'Alat "{alat.nama}" berhasil diperbarui!', 'success')
            return redirect(url_for('alat.index'))
        
        except ValueError:
            flash('Stok dan harga harus berupa angka!', 'danger')
            return redirect(url_for('alat.edit', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('alat.edit', id=id))
    
    return render_template('alat/form.html', action='Edit', alat=alat)


@alat_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    """Hapus alat"""
    alat = Alat.query.get_or_404(id)
    nama = alat.nama
    
    try:
        db.session.delete(alat)
        db.session.commit()
        flash(f'Alat "{nama}" berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('alat.index'))
