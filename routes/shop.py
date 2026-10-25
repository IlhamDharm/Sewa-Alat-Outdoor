from datetime import datetime
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import or_

from models.database import Alat, DetailSewa, Penyewa, Sewa, User, db

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')


def current_user():
    user_id = session.get('user_id')
    return db.session.get(User, user_id) if user_id else None


def user_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash('Masuk terlebih dahulu untuk melanjutkan.', 'info')
            return redirect(url_for('shop.login', next=request.full_path))
        return view(*args, **kwargs)
    return wrapped


def cart_items():
    cart = session.get('cart', {})
    items = []
    total = 0
    for alat_id, jumlah in cart.items():
        alat = db.session.get(Alat, int(alat_id))
        if not alat or alat.stok < 1:
            continue
        jumlah = min(max(int(jumlah), 1), alat.stok)
        items.append({'alat': alat, 'jumlah': jumlah, 'subtotal': alat.harga_per_hari * jumlah})
        total += alat.harga_per_hari * jumlah
    return items, total


@shop_bp.route('/')
def home():
    query = request.args.get('q', '').strip()
    kategori = request.args.get('kategori', '').strip()
    alat_query = Alat.query.filter(Alat.stok > 0)
    if query:
        alat_query = alat_query.filter(or_(Alat.nama.ilike(f'%{query}%'), Alat.kategori.ilike(f'%{query}%')))
    if kategori:
        alat_query = alat_query.filter_by(kategori=kategori)
    alat_list = alat_query.order_by(Alat.created_at.desc()).all()
    kategori_list = db.session.query(Alat.kategori).distinct().order_by(Alat.kategori).all()
    return render_template('shop/home.html', alat_list=alat_list, kategori_list=[row[0] for row in kategori_list], query=query, kategori=kategori, user=current_user())


@shop_bp.route('/alat/<int:id>')
def detail(id):
    alat = db.get_or_404(Alat, id)
    rekomendasi = Alat.query.filter(Alat.id != id, Alat.kategori == alat.kategori, Alat.stok > 0).limit(4).all()
    return render_template('shop/detail.html', alat=alat, rekomendasi=rekomendasi, user=current_user())


@shop_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user():
        return redirect(url_for('shop.home'))
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip().lower()
        no_hp = request.form.get('no_hp', '').strip()
        alamat = request.form.get('alamat', '').strip()
        password = request.form.get('password', '')
        if not all([nama, email, no_hp, alamat, password]) or len(password) < 6:
            flash('Lengkapi semua data. Password minimal 6 karakter.', 'danger')
            return render_template('shop/register.html')
        if User.query.filter_by(email=email).first():
            flash('Email tersebut sudah terdaftar.', 'warning')
            return render_template('shop/register.html')
        user = User(nama=nama, email=email, no_hp=no_hp, alamat=alamat)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        flash('Akun berhasil dibuat. Selamat datang!', 'success')
        return redirect(url_for('shop.home'))
    return render_template('shop/register.html')


@shop_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user():
        return redirect(url_for('shop.home'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(request.form.get('password', '')):
            session['user_id'] = user.id
            flash('Selamat datang kembali!', 'success')
            return redirect(request.args.get('next') or url_for('shop.home'))
        flash('Email atau password salah.', 'danger')
    return render_template('shop/login.html')


@shop_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('cart', None)
    flash('Anda telah keluar dari akun.', 'success')
    return redirect(url_for('shop.home'))


@shop_bp.route('/keranjang')
def cart():
    items, total = cart_items()
    return render_template('shop/cart.html', items=items, total=total, user=current_user())


@shop_bp.route('/keranjang/tambah/<int:id>', methods=['POST'])
def add_cart(id):
    alat = db.get_or_404(Alat, id)
    try:
        jumlah = max(1, int(request.form.get('jumlah', 1)))
    except (TypeError, ValueError):
        flash('Jumlah gear tidak valid.', 'danger')
        return redirect(request.referrer or url_for('shop.home'))
    if alat.stok < jumlah:
        flash(f'Stok {alat.nama} tersisa {alat.stok}.', 'warning')
    else:
        cart = session.setdefault('cart', {})
        cart[str(id)] = min(int(cart.get(str(id), 0)) + jumlah, alat.stok)
        session.modified = True
        flash(f'{alat.nama} ditambahkan ke keranjang.', 'success')
    return redirect(request.referrer or url_for('shop.home'))


@shop_bp.route('/keranjang/hapus/<int:id>', methods=['POST'])
def remove_cart(id):
    cart = session.get('cart', {})
    cart.pop(str(id), None)
    session['cart'] = cart
    return redirect(url_for('shop.cart'))


@shop_bp.route('/checkout', methods=['GET', 'POST'])
@user_required
def checkout():
    items, total = cart_items()
    if not items:
        flash('Keranjang masih kosong.', 'warning')
        return redirect(url_for('shop.home'))
    user = current_user()
    if request.method == 'POST':
        try:
            tanggal_sewa = datetime.strptime(request.form.get('tanggal_sewa', ''), '%Y-%m-%d')
            tanggal_kembali = datetime.strptime(request.form.get('tanggal_kembali', ''), '%Y-%m-%d')
        except (TypeError, ValueError):
            flash('Tanggal sewa dan tanggal kembali wajib diisi dengan benar.', 'danger')
            return render_template('shop/checkout.html', items=items, total=total, user=user)
        if tanggal_kembali <= tanggal_sewa:
            flash('Tanggal pengembalian harus setelah tanggal sewa.', 'danger')
            return render_template('shop/checkout.html', items=items, total=total, user=user)
        for item in items:
            if item['jumlah'] > item['alat'].stok:
                flash(f'Stok {item["alat"].nama} berubah. Silakan periksa kembali.', 'warning')
                return redirect(url_for('shop.cart'))
        penyewa = Penyewa.query.filter_by(no_hp=user.no_hp).first()
        if not penyewa:
            penyewa = Penyewa(nama=user.nama, no_hp=user.no_hp, alamat=user.alamat, jaminan='Data akun')
            db.session.add(penyewa)
            db.session.flush()
        jumlah_hari = max(1, (tanggal_kembali - tanggal_sewa).days)
        sewa = Sewa(user_id=user.id, penyewa_id=penyewa.id, tanggal_sewa=tanggal_sewa,
                    tanggal_rencana_kembali=tanggal_kembali, total_biaya=total * jumlah_hari,
                    status='aktif', order_status='menunggu')
        db.session.add(sewa)
        db.session.flush()
        for item in items:
            alat = item['alat']
            db.session.add(DetailSewa(sewa_id=sewa.id, alat_id=alat.id, jumlah=item['jumlah'],
                                      harga_satuan=alat.harga_per_hari,
                                      subtotal=alat.harga_per_hari * item['jumlah'] * jumlah_hari))
            alat.stok -= item['jumlah']
        db.session.commit()
        session['cart'] = {}
        return redirect(url_for('shop.order_detail', id=sewa.id))
    return render_template('shop/checkout.html', items=items, total=total, user=user)


@shop_bp.route('/pesanan')
@user_required
def orders():
    user = current_user()
    orders = Sewa.query.filter_by(user_id=user.id).order_by(Sewa.created_at.desc()).all()
    return render_template('shop/orders.html', orders=orders, user=user)


@shop_bp.route('/pesanan/<int:id>')
@user_required
def order_detail(id):
    user = current_user()
    order = Sewa.query.filter_by(id=id, user_id=user.id).first_or_404()
    return render_template('shop/order_detail.html', order=order, user=user)


@shop_bp.route('/akun')
@user_required
def account():
    return render_template('shop/account.html', user=current_user())
