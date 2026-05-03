from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from datetime import datetime, timedelta

import mysql.connector
import qrcode
import os
import random
import re

from fpdf import FPDF

app = Flask(__name__)
# ================= SECRET KEY =================
app.secret_key = os.getenv("SECRET_KEY", "elva")

# ================= KONEKSI DATABASE =================
def get_db_connection_elva():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
UPLOAD_FOLDER = 'static/upload_obat'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def role_required(role_list):
    def wrapper(f):
        def decorated(*args, **kwargs):
            if 'role_elva' not in session:
                return redirect(url_for('login_elva'))

            if session['role_elva'] not in role_list:
                return "Forbidden", 403

            return f(*args, **kwargs)
        decorated.__name__ = f.__name__
        return decorated
    return wrapper

def generate_struk_pdf(transaksi, detail):

    folder_path = os.path.join("static", "struk")
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{transaksi['no_faktur_elva']}.pdf")

    pdf = FPDF('P', 'mm', (80, 200))
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "APOTEK ELVA", ln=True, align="C")

    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 5, f"No Faktur : {transaksi['no_faktur_elva']}", ln=True)
    pdf.cell(0, 5, f"Tanggal   : {transaksi['tanggal_elva']}", ln=True)
    pdf.cell(0, 5, f"Pasien    : {transaksi.get('nama_lengkap_elva','-')}", ln=True)
    pdf.cell(0, 5, f"No Resep  : {transaksi.get('no_resep_elva','-')}", ln=True)
    pdf.ln(3)

    pdf.cell(0, 0, "-"*32, ln=True)
    pdf.ln(3)

    for item in detail:

        nama = item.get('nama_tampil', '-')
        jenis = item.get('jenis_tampil', '-')
        qty = item.get('jumlah_elva', 0)
        harga = int(item.get('harga_elva', 0))
        total = int(item.get('total_elva', 0))

        # Nama Obat
        pdf.set_font("Arial", "B", 9)
        pdf.multi_cell(0, 4, nama)

        pdf.set_font("Arial", "", 8)
        pdf.cell(0, 4, f"({jenis})", ln=True)

        # 🔥 Jika Racikan tampilkan dosis & catatan
        if item.get('is_racikan') == 1:

            dosis = item.get('dosis_elva') or '-'
            catatan = item.get('catatan_elva') or '-'

            pdf.cell(0, 4, f"Dosis: {dosis}", ln=True)
            pdf.multi_cell(0, 4, f"Catatan: {catatan}")

        pdf.cell(25, 5, f"{qty} x {harga:,}", 0)
        pdf.cell(0, 5, f"Rp {total:,}", 0, 1, "R")

        pdf.ln(2)

    pdf.cell(0, 0, "-"*32, ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 6, "TOTAL", 0)
    pdf.cell(0, 6, f"Rp {int(transaksi['total_elva']):,}", 0, 1, "R")

    pdf.ln(5)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "Terima Kasih", 0, 1, "C")

    pdf.output(file_path)

    return file_path

# ================== REGISTER ==================
@app.route('/register_elva', methods=['GET', 'POST'])
def register_elva():
    if request.method == 'POST':
        nama_elva = request.form['nama_elva']
        username_elva = request.form['username_elva']
        password_elva = generate_password_hash(request.form['password_elva'])
        role_elva = 'customer'

        conn = get_db_connection_elva()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id_user_elva FROM users_elva WHERE username_elva=%s",
            (username_elva,)
        )
        if cursor.fetchone():
            flash('Username sudah digunakan', 'danger')
            return redirect(url_for('register_elva'))

        cursor.execute("""
            INSERT INTO users_elva
            (nama_elva, username_elva, password_elva, role_elva)
            VALUES (%s,%s,%s,%s)
        """, (nama_elva, username_elva, password_elva, role_elva))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Registrasi berhasil, silakan login', 'success')
        return redirect(url_for('login_elva'))

    return render_template('register_elva.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login_elva', methods=['GET', 'POST'])
def login_elva():

    if request.method == 'POST':
        username = request.form['username_elva']
        password = request.form['password_elva']

        conn = get_db_connection_elva()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users_elva WHERE username_elva=%s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_elva'], password):

            # Simpan session
            session['user_online_elva'] = user['id_user_elva']
            session['nama_online_elva'] = user['nama_elva']
            session['role_elva'] = user['role_elva']

            # ======================
            # REDIRECT SESUAI ROLE
            # ======================

            if user['role_elva'] == 'admin':
                return redirect(url_for('dashboard_admin_elva'))

            elif user['role_elva'] == 'kasir':
                return redirect(url_for('kasir_offline_elva'))

            elif user['role_elva'] == 'customer':
                return redirect(url_for('shop_online_elva'))
            elif user['role_elva'] == 'kurir':
                return redirect(url_for('kurir_dashboard_elva'))
            else:
                flash('Role tidak dikenali', 'danger')
                return redirect(url_for('login_elva'))

        flash('Username atau password salah', 'danger')

    return render_template('login_elva.html')
from collections import OrderedDict

# ================= DASHBOARD ADMIN =================
@app.route('/dashboard_admin_elva')
@role_required(['admin', 'super_admin'])
def dashboard_admin_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    # ================= STATISTIK =================
    cursor.execute("SELECT COUNT(*) FROM users_elva WHERE role_elva!='admin'")
    total_user = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM obat_elva")
    total_obat = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transaksi_elva")
    total_transaksi = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(SUM(total_elva),0) FROM transaksi_elva")
    total_pendapatan = cursor.fetchone()[0]

    # ================= GRAFIK PENJUALAN PER BULAN =================
    cursor.execute("""
        SELECT DATE_FORMAT(tanggal_elva, '%b') AS bulan,
               SUM(total_elva) as total
        FROM transaksi_elva
        GROUP BY MONTH(tanggal_elva)
        ORDER BY MONTH(tanggal_elva)
    """)

    hasil = cursor.fetchall()

    labels = []
    values = []

    for row in hasil:
        labels.append(row[0])
        values.append(float(row[1]))

    cursor.close()
    conn.close()

    return render_template(
        'dashboard_admin_elva.html',
        total_user=total_user,
        total_obat=total_obat,
        total_transaksi=total_transaksi,
        total_pendapatan=total_pendapatan,
        labels=labels,
        values=values
    )

# =========================
# DATA USER
# =========================
@app.route('/admin_user_elva')
@role_required(['admin', 'super_admin'])
def admin_user_elva():
    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users_elva")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_user_elva.html', users=users)


# =========================
# RESET PASSWORD
# =========================
@app.route('/reset_password_user_elva/<int:id>', methods=['POST'])
@role_required(['admin', 'super_admin'])
def reset_password_user_elva(id):

    # Tidak bisa reset password sendiri
    if session.get('user_online_elva') == id:
        flash("Tidak bisa reset password sendiri!", "warning")
        return redirect(url_for('admin_user_elva'))

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # Ambil data target
    cursor.execute("SELECT role_elva FROM users_elva WHERE id_user_elva=%s", (id,))
    target = cursor.fetchone()

    if not target:
        flash("User tidak ditemukan!", "danger")
        return redirect(url_for('admin_user_elva'))

    # Admin tidak boleh reset Super Admin
    if session.get('role_elva') == 'admin' and target['role_elva'] == 'super_admin':
        flash("Admin tidak bisa reset password Super Admin!", "danger")
        return redirect(url_for('admin_user_elva'))

    password_baru = request.form['password_baru']
    password_hash = generate_password_hash(password_baru)

    cursor.execute("""
        UPDATE users_elva 
        SET password_elva=%s 
        WHERE id_user_elva=%s
    """, (password_hash, id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Password berhasil diperbarui!", "success")
    return redirect(url_for('admin_user_elva'))


# =========================
# HAPUS USER
# =========================
@app.route('/hapus_user_elva/<int:id>')
@role_required(['admin','super_admin'])
def hapus_user_elva(id):

    # Tidak boleh hapus diri sendiri
    if session.get('user_online_elva') == id:
        flash("Anda tidak bisa menghapus akun sendiri!", "warning")
        return redirect(url_for('admin_user_elva'))

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users_elva WHERE id_user_elva=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("User berhasil dihapus", "danger")
    return redirect(url_for('admin_user_elva'))


# =========================
# EDIT USER
# =========================
@app.route('/edit_user_elva/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'super_admin'])
def edit_user_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nama = request.form['nama']
        role = request.form['role']

        # Cegah admin mengubah super_admin
        cursor.execute("SELECT role_elva FROM users_elva WHERE id_user_elva=%s", (id,))
        target = cursor.fetchone()

        if session.get('role_elva') == 'admin' and target['role_elva'] == 'super_admin':
            flash("Admin tidak bisa mengedit Super Admin!", "danger")
            return redirect(url_for('admin_user_elva'))

        cursor.execute("""
            UPDATE users_elva 
            SET nama_elva=%s, role_elva=%s
            WHERE id_user_elva=%s
        """, (nama, role, id))

        conn.commit()
        flash("Data user berhasil diperbarui", "success")
        return redirect(url_for('admin_user_elva'))

    cursor.execute("SELECT * FROM users_elva WHERE id_user_elva=%s", (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit_user_elva.html', user=user)


# =========================
# TAMBAH USER
# =========================
@app.route('/tambah_user_elva', methods=['POST'])
@role_required(['admin', 'super_admin'])
def tambah_user_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    nama = request.form['nama']
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    role = request.form['role']

    cursor.execute("""
        INSERT INTO users_elva 
        (nama_elva, username_elva, password_elva, role_elva)
        VALUES (%s, %s, %s, %s)
    """, (nama, username, password, role))

    conn.commit()
    cursor.close()
    conn.close()

    flash("User berhasil ditambahkan", "success")
    return redirect(url_for('admin_user_elva'))

@app.route('/admin_obat_elva')
@role_required(['admin','super_admin'])
def admin_obat_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT obat_elva.*, kategori_elva.nama_kategori_elva
        FROM obat_elva
        JOIN kategori_elva 
        ON obat_elva.kategori_id_elva = kategori_elva.id_kategori_elva
    """)
    obat = cursor.fetchall()

    # ambil kategori untuk modal
    cursor.execute("SELECT * FROM kategori_elva")
    kategori = cursor.fetchall()

    cursor.execute("SELECT * FROM gudang_elva")
    gudang = cursor.fetchall()

    return render_template(
        'admin_obat_elva.html',
        obat=obat,
        kategori=kategori,
        gudang=gudang
    )
@app.route('/tambah_obat_elva', methods=['POST'])
@role_required(['admin', 'super_admin'])
def tambah_obat_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    nama = request.form['nama_obat_elva']
    harga = request.form['harga_elva']
    stok = request.form['stok_elva']
    kategori = request.form['kategori_id_elva']
    tanggal_exp_elva = request.form['tanggal_exp_elva']
    gudang_id = request.form['gudang_id_elva']  # ✅ ambil gudang

    # ================== AUTO GENERATE KODE ==================
    cursor.execute("""
        SELECT kode_obat_elva 
        FROM obat_elva 
        ORDER BY id_obat_elva DESC 
        LIMIT 1
    """)
    last_kode = cursor.fetchone()

    if last_kode:
        angka = int(last_kode[0][3:])
        angka += 1
    else:
        angka = 1

    kode_obat = f"OBT{angka:03d}"
    # ========================================================

    file = request.files['upload_obat']
    filename = file.filename

    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    cursor.execute("""
        INSERT INTO obat_elva
        (kode_obat_elva, nama_obat_elva, jenis_obat_elva, harga_elva, stok_elva,
         kategori_id_elva, gambar_elva, tanggal_exp_elva, id_gudang_elva)
        VALUES (%s,%s,'jadi',%s,%s,%s,%s,%s,%s)
    """,(kode_obat, nama, harga, stok, kategori, filename, tanggal_exp_elva, gudang_id))

    conn.commit()

    return redirect(url_for('admin_obat_elva'))

@app.route('/hapus_obat_elva/<int:id>')
@role_required(['admin', 'super_admin'])
def hapus_obat_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM obat_elva WHERE id_obat_elva=%s",(id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_obat_elva'))
@app.route('/edit_obat_elva/<int:id>', methods=['POST'])
@role_required(['admin', 'super_admin'])
def edit_obat_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    nama = request.form['nama_obat_elva']
    harga = request.form['harga_elva']
    stok = request.form['stok_elva']
    kategori = request.form['kategori_id_elva']
    tanggal_exp = request.form['tanggal_exp_elva']
    gudang_id = request.form['gudang_id_elva']

    # cek apakah upload gambar baru
    file = request.files['upload_obat']

    if file and file.filename != '':
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        cursor.execute("""
            UPDATE obat_elva SET
            nama_obat_elva=%s,
            harga_elva=%s,
            stok_elva=%s,
            kategori_id_elva=%s,
            tanggal_exp_elva=%s,
            id_gudang_elva=%s,
            gambar_elva=%s
            WHERE id_obat_elva=%s
        """, (nama, harga, stok, kategori, tanggal_exp,
              gudang_id, filename, id))
    else:
        cursor.execute("""
            UPDATE obat_elva SET
            nama_obat_elva=%s,
            harga_elva=%s,
            stok_elva=%s,
            kategori_id_elva=%s,
            tanggal_exp_elva=%s,
            id_gudang_elva=%s
            WHERE id_obat_elva=%s
        """, (nama, harga, stok, kategori,
              tanggal_exp, gudang_id, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_obat_elva'))

@app.route('/admin_kategori_elva', methods=['GET', 'POST'])
@role_required(['admin', 'super_admin'])
def admin_kategori_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # ================= TAMBAH =================
    if request.method == "POST":
        nama = request.form.get("nama_kategori_elva")
        edit_id = request.form.get("edit_id")

        if edit_id:  # UPDATE
            cursor.execute("""
                UPDATE kategori_elva 
                SET nama_kategori_elva = %s
                WHERE id_kategori_elva = %s
            """, (nama, edit_id))
            conn.commit()
            flash("Kategori berhasil diupdate!", "success")

        else:  # INSERT
            cursor.execute("""
                INSERT INTO kategori_elva (nama_kategori_elva)
                VALUES (%s)
            """, (nama,))
            conn.commit()
            flash("Kategori berhasil ditambahkan!", "success")

        cursor.close()
        conn.close()
        return redirect(url_for('admin_kategori_elva'))

    # ================= TAMPIL DATA =================
    cursor.execute("SELECT * FROM kategori_elva")
    kategori = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_kategori_elva.html', kategori=kategori)
@app.route('/hapus_kategori_elva/<int:id>')
@role_required(['admin', 'super_admin'])
def hapus_kategori_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM kategori_elva WHERE id_kategori_elva = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Kategori berhasil dihapus!", "danger")
    return redirect(url_for('admin_kategori_elva'))

    # transaksi
@app.route('/admin_transaksi_elva')
@role_required(['admin','super_admin'])
def admin_transaksi_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        t.*,
        CASE
            WHEN t.tipe_elva = 'online' 
                THEN u.nama_elva
            ELSE p.nama_lengkap_elva
        END AS nama_customer,
        pg.no_resi_elva,
        pg.status_elva AS status_pengiriman,
        uk.nama_elva AS nama_kurir
    FROM transaksi_elva t
    LEFT JOIN pasien_elva p 
        ON p.id_pasien_elva = t.id_pasien_elva
    LEFT JOIN users_elva u
        ON u.id_user_elva = t.id_user_elva
    LEFT JOIN pengiriman_elva pg 
        ON pg.id_transaksi_elva = t.id_transaksi_elva
    LEFT JOIN users_elva uk
        ON uk.id_user_elva = pg.id_kurir_elva
    ORDER BY t.id_transaksi_elva DESC
    """)

    transaksi = cursor.fetchall()

    # Tambahkan nama file QR
    for t in transaksi:
        if t['tipe_elva'] == 'online' and t['no_resi_elva']:
            t['qr_file'] = f"{t['no_resi_elva']}.png"
        else:
            t['qr_file'] = None

    for t in transaksi:
        if t['no_faktur_elva']:
            file_path = f"static/struk/{t['no_faktur_elva']}.pdf"
            t['struk_exist'] = os.path.exists(file_path)
        else:
            t['struk_exist'] = False

    cursor.close()
    conn.close()

    return render_template('admin_transaksi_elva.html', transaksi=transaksi)


@app.route('/admin_pengiriman_elva')
@role_required(['admin','super_admin'])
def admin_pengiriman_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        t.id_transaksi_elva,
        t.no_faktur_elva,
        t.tanggal_elva,
        t.alamat_elva,
        t.total_elva,
        t.metode_bayar_elva,
        t.status_elva,
        u.nama_elva AS customer,

        pg.id_pengiriman_elva,
        pg.no_resi_elva,

        CASE 
            WHEN pg.status_elva IS NULL 
                 OR pg.status_elva = '' 
            THEN 'menunggu_verifikasi'
            ELSE LOWER(pg.status_elva)
        END AS status_pengiriman_elva,

        pg.foto_bukti_elva,
        kurir.nama_elva AS nama_kurir

    FROM transaksi_elva t

    LEFT JOIN users_elva u
        ON u.id_user_elva = t.id_user_elva

    LEFT JOIN pengiriman_elva pg
        ON pg.id_transaksi_elva = t.id_transaksi_elva

    LEFT JOIN users_elva kurir
        ON kurir.id_user_elva = pg.id_kurir_elva
        AND kurir.role_elva = 'kurir'

    WHERE t.tipe_elva = 'online'
    AND t.kurir_elva != 'Ambil Sendiri'

    ORDER BY t.id_transaksi_elva DESC
    """)

    pengiriman = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_pengiriman_elva.html',
        pengiriman=pengiriman
    )
@app.route('/admin_kemas_elva/<int:id_pengiriman>', methods=['POST'])
@role_required(['admin','super_admin'])
def admin_kemas_elva(id_pengiriman):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    # 🔹 Update pengiriman
    cursor.execute("""
        UPDATE pengiriman_elva
        SET status_elva='dikemas',
            keterangan_elva='Paket sedang dikemas'
        WHERE id_pengiriman_elva=%s
    """, (id_pengiriman,))

    # 🔹 Update transaksi
    cursor.execute("""
        UPDATE transaksi_elva t
        JOIN pengiriman_elva p
        ON t.id_transaksi_elva = p.id_transaksi_elva
        SET t.status_pengiriman_elva='dikemas'
        WHERE p.id_pengiriman_elva=%s
    """, (id_pengiriman,))

    # 🔥 INSERT TRACKING
    cursor.execute("""
        INSERT INTO tracking_pengiriman_elva
        (id_pengiriman_elva, status_tracking, keterangan_tracking, waktu_tracking)
        VALUES (%s, %s, %s, NOW())
    """, (
        id_pengiriman,
        'dikemas',
        'Paket sedang dikemas'
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_pengiriman_elva'))
@app.route('/admin_kirim_elva/<int:id_pengiriman>', methods=['POST'])
@role_required(['admin','super_admin'])
def admin_kirim_elva(id_pengiriman):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    # 🔹 Update pengiriman
    cursor.execute("""
        UPDATE pengiriman_elva
        SET status_elva='diserahkan_ke_kurir',
            keterangan_elva='Paket telah diserahkan kepada kurir'
        WHERE id_pengiriman_elva=%s
    """, (id_pengiriman,))

    # 🔹 Update transaksi
    cursor.execute("""
        UPDATE transaksi_elva t
        JOIN pengiriman_elva p
        ON t.id_transaksi_elva = p.id_transaksi_elva
        SET t.status_pengiriman_elva='diserahkan_ke_kurir'
        WHERE p.id_pengiriman_elva=%s
    """, (id_pengiriman,))

    # 🔥 INSERT TRACKING
    cursor.execute("""
        INSERT INTO tracking_pengiriman_elva
        (id_pengiriman_elva, status_tracking, keterangan_tracking, waktu_tracking)
        VALUES (%s, %s, %s, NOW())
    """, (
        id_pengiriman,
        'diserahkan_ke_kurir',
        'Paket telah diserahkan kepada kurir'
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_pengiriman_elva'))
@app.route('/admin_verifikasi_elva/<int:id_pengiriman>', methods=['POST'])
@role_required(['admin','super_admin'])
def admin_verifikasi_elva(id_pengiriman):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    # 🔹 Update pengiriman
    cursor.execute("""
        UPDATE pengiriman_elva
        SET status_elva='diverifikasi',
            keterangan_elva='Pesanan telah diverifikasi admin'
        WHERE id_pengiriman_elva=%s
    """, (id_pengiriman,))

    # 🔹 Update transaksi
# 🔹 Update transaksi
    cursor.execute("""
        UPDATE transaksi_elva t
        JOIN pengiriman_elva p
        ON t.id_transaksi_elva = p.id_transaksi_elva
        SET 
            t.status_pengiriman_elva = 'diverifikasi',
            t.status_elva = 'diproses',
            t.status_verifikasi_elva = 'sudah_verifikasi'
        WHERE p.id_pengiriman_elva = %s
    """, (id_pengiriman,))
    # 🔥 Tracking
    cursor.execute("""
        INSERT INTO tracking_pengiriman_elva
        (id_pengiriman_elva, status_tracking, keterangan_tracking, waktu_tracking)
        VALUES (%s, %s, %s, NOW())
    """, (
        id_pengiriman,
        'diverifikasi',
        'Pesanan telah diverifikasi admin'
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_pengiriman_elva'))
@app.route('/scan_qr_elva', methods=['POST'])
@role_required(['admin','super_admin'])
def scan_qr_elva():

    data = request.get_json()
    qr_code = data.get('qr_code')

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # Cari transaksi berdasarkan faktur
    cursor.execute("""
        SELECT id_transaksi_elva, status_elva
        FROM transaksi_elva
        WHERE no_faktur_elva = %s
    """, (qr_code.strip(),))

    transaksi = cursor.fetchone()

    if not transaksi:
        cursor.close()
        conn.close()
        return jsonify({"status": "invalid"})

    # Cegah scan ulang
    if transaksi['status_elva'] == 'selesai':
        cursor.close()
        conn.close()
        return jsonify({"status": "already"})

    now = datetime.now()

    cursor.execute("""
        UPDATE transaksi_elva
        SET status_elva = 'selesai',
            waktu_selesai_elva = %s
        WHERE id_transaksi_elva = %s
    """, (now, transaksi['id_transaksi_elva']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "waktu": now.strftime("%d-%m-%Y %H:%M:%S")
    })


@app.route('/update_status_elva/<int:id>', methods=['POST'])
@role_required(['admin', 'super_admin'])
def update_status_elva(id):
    status = request.form['status_elva']

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transaksi_elva
        SET status_elva=%s
        WHERE id_transaksi_elva=%s
    """,(status,id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_transaksi_elva'))

# ================== SHOP ==================
@app.route('/shop_online_elva')
def shop_online_elva():
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    search_elva = request.args.get('search_elva', '')
    kategori_elva_id = request.args.get('kategori_elva', '')

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT o.*, k.nama_kategori_elva
        FROM obat_elva o
        JOIN kategori_elva k ON k.id_kategori_elva=o.kategori_id_elva
        WHERE 1=1
    """
    params = []

    if search_elva:
        query += " AND o.nama_obat_elva LIKE %s"
        params.append(f"%{search_elva}%")

    if kategori_elva_id:
        query += " AND o.kategori_id_elva=%s"
        params.append(int(kategori_elva_id))

    cursor.execute(query, params)
    obat_elva = cursor.fetchall()

    cursor.execute("SELECT * FROM kategori_elva")
    kategori_elva = cursor.fetchall()
    # 🔹 Ambil PESANAN AKTIF
    cursor.execute("""
    SELECT 
        t.id_transaksi_elva,
        t.no_faktur_elva,
        t.tanggal_elva,
        t.total_elva,
        t.status_elva,
        COALESCE(p.status_elva, 'menunggu_verifikasi') AS status_pengiriman,
        t.kurir_elva,
        p.no_resi_elva
    FROM transaksi_elva t
    LEFT JOIN pengiriman_elva p
        ON p.id_transaksi_elva = t.id_transaksi_elva
    WHERE t.id_user_elva=%s
    AND t.tipe_elva='online'
    AND (
        p.status_elva IS NULL
        OR p.status_elva NOT IN ('sampai')
    )
    ORDER BY t.id_transaksi_elva DESC
    LIMIT 5
    """, (session['user_online_elva'],))
    list_pesanan = cursor.fetchall()
    cursor.execute("""
    SELECT 
        t.id_transaksi_elva,
        t.no_faktur_elva,
        t.tanggal_elva,
        t.total_elva
    FROM transaksi_elva t
    WHERE t.id_user_elva=%s
    AND t.tipe_elva='online'
    AND t.status_pengiriman_elva IN ('sampai','selesai')
    ORDER BY t.id_transaksi_elva DESC
""", (session['user_online_elva'],))

    riwayat_transaksi = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
    'shop_elva.html',
    list_pesanan=list_pesanan,
    riwayat_transaksi=riwayat_transaksi,
    obat_elva=obat_elva,
    kategori_elva=kategori_elva
)
@app.route('/riwayat_transaksi_elva')
def riwayat_transaksi_elva():

    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        t.id_transaksi_elva,
        t.no_faktur_elva,
        t.tanggal_elva,
        t.total_elva
    FROM transaksi_elva t
    LEFT JOIN pengiriman_elva p
        ON p.id_transaksi_elva = t.id_transaksi_elva
    WHERE t.id_user_elva=%s
    AND t.tipe_elva='online'
    AND p.status_elva = 'sampai'
    ORDER BY t.id_transaksi_elva DESC
    """, (session['user_online_elva'],))
    riwayat = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("riwayat_transaksi_elva.html", riwayat=riwayat)


# ================== ADD CART ==================
@app.route('/add_cart_elva', methods=['POST'])
def add_cart_elva():
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    id_obat_elva = request.form['id_obat_elva']
    nama_obat_elva = request.form['nama_obat_elva']
    harga_elva = int(request.form['harga_elva'])

    cart = session.get('cart_elva', [])

    for item in cart:
        if item['id_obat_elva'] == id_obat_elva:
            item['jumlah_elva'] += 1
            session['cart_elva'] = cart
            return redirect(url_for('shop_online_elva'))

    cart.append({
        'id_obat_elva': id_obat_elva,
        'nama_obat_elva': nama_obat_elva,
        'harga_elva': harga_elva,
        'jumlah_elva': 1
    })

    session['cart_elva'] = cart
    return redirect(url_for('shop_online_elva'))


# ================== CART ==================
@app.route('/cart_elva')
def cart_elva():
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    cart = session.get('cart_elva', [])

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # 🔥 Tambahkan stok ke setiap item
    for item in cart:
        cursor.execute(
            "SELECT stok_elva FROM obat_elva WHERE id_obat_elva=%s",
            (item['id_obat_elva'],)
        )
        data = cursor.fetchone()
        item['stok_elva'] = data['stok_elva'] if data else 0

    cursor.close()
    conn.close()

    total = sum(i['harga_elva'] * i['jumlah_elva'] for i in cart)

    return render_template(
        'cart_elva.html',
        cart_elva=cart,
        total_elva=total
    )

@app.route('/delete_cart_elva', methods=['POST'])
def delete_cart_elva():
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    selected_ids = request.form.getlist('selected_item')
    cart = session.get('cart_elva', [])

    new_cart = [
        item for item in cart
        if str(item['id_obat_elva']) not in selected_ids
    ]

    session['cart_elva'] = new_cart
    session.modified = True

    flash('Item berhasil dihapus dari keranjang', 'success')
    return redirect(url_for('cart_elva'))

@app.route('/increase_qty_elva/<id_obat>', methods=['POST'])
def increase_qty_elva(id_obat):
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    cart = session.get('cart_elva', [])

    # 🔹 Ambil stok dari database
    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT stok_elva FROM obat_elva WHERE id_obat_elva=%s",
        (id_obat,)
    )
    data_obat = cursor.fetchone()
    cursor.close()
    conn.close()

    if not data_obat:
        flash("Obat tidak ditemukan", "danger")
        return redirect(url_for('cart_elva'))

    stok_db = data_obat['stok_elva']

    for item in cart:
        if str(item['id_obat_elva']) == str(id_obat):

            # 🔥 CEK STOK
            if item['jumlah_elva'] >= stok_db:
                flash("Jumlah melebihi stok yang tersedia!", "warning")
            else:
                item['jumlah_elva'] += 1

            break

    session['cart_elva'] = cart
    session.modified = True

    return redirect(url_for('cart_elva'))

@app.route('/decrease_qty_elva/<id_obat>', methods=['POST'])
def decrease_qty_elva(id_obat):
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    cart = session.get('cart_elva', [])

    for item in cart[:]:
        if str(item['id_obat_elva']) == str(id_obat):

            # Kalau lebih dari 1 → kurangi
            if item['jumlah_elva'] > 1:
                item['jumlah_elva'] -= 1
            else:
                # Kalau sudah 1 → hapus item
                cart.remove(item)

            break

    session['cart_elva'] = cart
    session.modified = True

    return redirect(url_for('cart_elva'))

@app.route('/checkout_form_elva')
def checkout_form_elva():
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    cart_elva = session.get('cart_elva', [])
    if not cart_elva:
        flash('Keranjang masih kosong', 'warning')
        return redirect(url_for('shop_online_elva'))

    subtotal_elva = sum(i['harga_elva'] * i['jumlah_elva'] for i in cart_elva)
    pajak_elva = int(subtotal_elva * 0.1)

    # 🔹 KURIR DARI QUERY STRING
    kurir_raw = request.args.get('kurir_elva', '')
    ongkir_elva = 0
    kurir_elva = ''

    if kurir_raw:
        kurir_elva, ongkir_elva = kurir_raw.split('|')
        ongkir_elva = int(ongkir_elva)

    diskon_elva = 0
    if subtotal_elva >= 50000:
        diskon_elva = int(subtotal_elva * 0.1)  # 10%

    total_sementara_elva = subtotal_elva + pajak_elva + ongkir_elva - diskon_elva

    return render_template(
        'checkout_form_elva.html',
        cart_elva=cart_elva,
        subtotal_elva=subtotal_elva,
        pajak_elva=pajak_elva,
        ongkir_elva=ongkir_elva,
        total_sementara_elva=total_sementara_elva,
        kurir_elva=kurir_elva,
        diskon_elva=diskon_elva,
        nama_elva=session['nama_online_elva']
    )
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/bukti_bayar'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

# ================= CONFIG =================
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
UPLOAD_FOLDER = 'static/bukti_bayar'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/checkout_online_elva', methods=['POST'])
def checkout_online_elva():

    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    try:
        # ================= INPUT =================
        alamat_elva = request.form.get('alamat_elva', '').strip()
        metode_bayar_elva = request.form.get('metode_bayar_elva')
        metode_detail = request.form.get('metode_transfer')
        kurir_raw = request.form.get('kurir_elva')

        # ================= VALIDASI =================
        if metode_bayar_elva != "TRANSFER":
            flash("Metode pembayaran harus transfer!", "danger")
            return redirect(url_for('checkout_form_elva'))

        if not metode_detail:
            flash("Pilih metode transfer dulu!", "danger")
            return redirect(url_for('checkout_form_elva'))

        if not kurir_raw or '|' not in kurir_raw:
            flash("Kurir tidak valid!", "danger")
            return redirect(url_for('checkout_form_elva'))

        # ================= FILE =================
        file = request.files.get('bukti_bayar_elva')

        if not file or file.filename == '':
            flash("Bukti pembayaran wajib diupload!", "danger")
            return redirect(url_for('checkout_form_elva'))

        if not allowed_file(file.filename):
            flash("Format file harus gambar!", "danger")
            return redirect(url_for('checkout_form_elva'))

        filename = f"{int(datetime.now().timestamp())}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        db_filepath = f"bukti_bayar/{filename}"

        # ================= KURIR =================
        kurir_elva, ongkir_elva = kurir_raw.split('|')
        ongkir_elva = int(ongkir_elva)

        tanggal_pengambilan = None
        if kurir_elva.lower() == "ambil sendiri":
            tanggal_pengambilan = datetime.now() + timedelta(days=1)

        # ================= CART =================
        cart = session.get('cart_elva', [])
        if not cart:
            flash("Keranjang kosong!", "danger")
            return redirect(url_for('shop_online_elva'))

        # ================= HITUNG =================
        id_user_elva = session['user_online_elva']
        no_faktur_elva = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        total_barang = sum(i['harga_elva'] * i['jumlah_elva'] for i in cart)
        pajak = int(total_barang * 0.1)
        diskon = int(total_barang * 0.1) if total_barang >= 50000 else 0
        grand_total = total_barang + pajak + ongkir_elva - diskon

        # ================= INSERT TRANSAKSI =================
        cursor.execute("""
            INSERT INTO transaksi_elva (
                no_faktur_elva,
                tanggal_elva,
                id_user_elva,
                alamat_elva,
                metode_bayar_elva,
                metode_detail_elva,
                kurir_elva,
                ongkir_elva,
                total_elva,
                tipe_elva,
                status_elva,
                status_verifikasi_elva,
                bukti_bayar_elva,
                tanggal_pengambilan_elva
            )
            VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s,
                    'online', %s, %s, %s, %s)
        """, (
            no_faktur_elva,
            id_user_elva,
            alamat_elva,
            metode_bayar_elva,
            metode_detail,
            kurir_elva,
            ongkir_elva,
            grand_total,
            'menunggu_verifikasi',
            'menunggu',
            db_filepath,
            tanggal_pengambilan
        ))

        id_transaksi = cursor.lastrowid

        # ================= DETAIL =================
        for item in cart:
            cursor.execute("""
                INSERT INTO transaksi_detail_elva
                (id_transaksi_elva, id_obat_elva, jumlah_elva, harga_elva, total_elva)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                id_transaksi,
                item['id_obat_elva'],
                item['jumlah_elva'],
                item['harga_elva'],
                item['harga_elva'] * item['jumlah_elva']
            ))

        # ================= RESI =================
        no_resi_elva = f"ELVA-{datetime.now().strftime('%Y%m%d')}-{id_transaksi}"

        qr_path_db = None

        # ================= QR RESI (HANYA ANTAR) =================
        if kurir_elva.lower() != "ambil sendiri":
            import qrcode

            qr_folder = 'static/qr_resi_elva'
            os.makedirs(qr_folder, exist_ok=True)

            qr_data = f"RESI:{no_resi_elva}|ID:{id_transaksi}"
            qr_filename = f"{no_resi_elva}.png"

            qr_full_path = os.path.join(qr_folder, qr_filename)

            qr_img = qrcode.make(qr_data)
            qr_img.save(qr_full_path)

            qr_path_db = f"qr_resi_elva/{qr_filename}"

        # ================= INSERT PENGIRIMAN =================
        cursor.execute("""
            INSERT INTO pengiriman_elva
            (id_transaksi_elva, no_resi_elva, status_elva, keterangan_elva, qr_resi_elva)
            VALUES (%s,%s,'menunggu','Menunggu verifikasi pembayaran', %s)
        """, (
            id_transaksi,
            no_resi_elva,
            qr_path_db
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("ERROR CHECKOUT:", e)
        flash(f"Terjadi kesalahan: {str(e)}", "danger")
        return redirect(url_for('checkout_form_elva'))

    finally:
        cursor.close()
        conn.close()

    # ================= CLEAR =================
    session.pop('cart_elva', None)

    flash('Pesanan berhasil dibuat, menunggu verifikasi pembayaran', 'success')
    return redirect(url_for('shop_online_elva'))
@app.route('/kasir_verifikasi_elva')
@role_required(['kasir'])
def kasir_verifikasi_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM transaksi_elva
        WHERE status_verifikasi_elva='menunggu'
        ORDER BY tanggal_elva DESC
    """)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('kasir_verifikasi_elva.html', data=data)
@app.route('/verifikasi/<int:id>')
@role_required(['kasir'])
def verifikasi(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transaksi_elva
        SET status_verifikasi_elva='verified',
            status_elva='diproses'
        WHERE id_transaksi_elva=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Pembayaran berhasil diverifikasi", "success")
    return redirect(url_for('kasir_verifikasi_elva'))
@app.route('/kurir_scan_resi_elva', methods=['POST'])
@role_required(['kurir'])
def kurir_scan_resi_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    try:
        no_resi_raw = request.form.get('no_resi', '')
        foto = request.files.get('foto_bukti')

        if not no_resi_raw:
            return jsonify({"status": "error", "message": "Resi kosong"})

        # 🔹 Extract resi dari QR
        if "RESI:" in no_resi_raw:
            no_resi = no_resi_raw.split("RESI:")[1].split("|")[0]
        else:
            no_resi = no_resi_raw.split("|")[0]

        no_resi = re.sub(r'[^A-Za-z0-9\-]', '', no_resi)

        if not no_resi:
            return jsonify({"status": "error", "message": "Format resi tidak valid"})

        # 🔹 Ambil data pengiriman
        cursor.execute("""
            SELECT * FROM pengiriman_elva
            WHERE no_resi_elva=%s
        """, (no_resi,))
        data = cursor.fetchone()

        if not data:
            return jsonify({"status": "error", "message": "Resi tidak ditemukan"})

        id_pengiriman = data['id_pengiriman_elva']
        id_transaksi = data['id_transaksi_elva']
        status = data['status_elva']
        id_kurir_login = session.get('user_online_elva')

        if not id_kurir_login:
            return jsonify({"status": "error", "message": "Session login tidak ditemukan"})

        # 🔒 Sudah selesai?
        if status == 'sampai':
            return jsonify({"status": "error", "message": "Pengiriman sudah selesai"})

        # 🔒 Cek kurir lain
        if data['id_kurir_elva'] and data['id_kurir_elva'] != id_kurir_login:
            return jsonify({"status": "error", "message": "Paket sudah diambil kurir lain"})
        # ==========================================
        # 🔒 BATAS MAKSIMAL 10 PAKET AKTIF
        # ==========================================
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM pengiriman_elva
            WHERE id_kurir_elva=%s
            AND status_elva IN ('diserahkan_ke_kurir','dalam_perjalanan')
        """, (id_kurir_login,))

        jumlah_paket = cursor.fetchone()['total']

        # Jika scan pertama & sudah 10 paket
        if status == 'diserahkan_ke_kurir' and jumlah_paket >= 10:
            return jsonify({
                "status": "error",
                "message": "Maksimal 10 paket aktif. Selesaikan dulu paket sebelumnya."
            })

        # =====================================================
        # 1️⃣ Scan pertama → dalam_perjalanan
        # =====================================================
        if status == 'diserahkan_ke_kurir':

            new_status = 'dalam_perjalanan'
            ket = 'Sedang menuju alamat tujuan'

            cursor.execute("""
                UPDATE pengiriman_elva
                SET status_elva=%s,
                    keterangan_elva=%s,
                    id_kurir_elva=%s
                WHERE id_pengiriman_elva=%s
            """, (new_status, ket, id_kurir_login, id_pengiriman))

            # Update transaksi
            cursor.execute("""
                UPDATE transaksi_elva
                SET status_pengiriman_elva=%s
                WHERE id_transaksi_elva=%s
            """, (new_status, id_transaksi))

        # =====================================================
        # 2️⃣ Scan kedua → sampai (WAJIB FOTO)
        # =====================================================
        elif status == 'dalam_perjalanan':

            if not foto:
                return jsonify({
                    "status": "need_photo",
                    "message": "Upload foto bukti untuk menyelesaikan pengiriman."
                })

            new_status = 'sampai'
            ket = 'Paket telah sampai ke tujuan'

            # Simpan foto
            folder = "static/bukti_pengiriman"
            os.makedirs(folder, exist_ok=True)

            filename = secure_filename(no_resi + ".jpg")
            path = os.path.join(folder, filename)
            foto.save(path)

            # Update pengiriman
            cursor.execute("""
                UPDATE pengiriman_elva
                SET status_elva=%s,
                    keterangan_elva=%s,
                    id_kurir_elva=%s,
                    foto_bukti_elva=%s
                WHERE id_pengiriman_elva=%s
            """, (new_status, ket, id_kurir_login, filename, id_pengiriman))

            # 🔥 AUTO SELESAI + AUTO LUNAS
            cursor.execute("""
                UPDATE transaksi_elva
                SET status_pengiriman_elva=%s,
                    status_elva='selesai',
                    waktu_selesai_elva=NOW(),
                    status_pembayaran_elva='lunas'
                WHERE id_transaksi_elva=%s
            """, (new_status, id_transaksi))

        else:
            return jsonify({
                "status": "error",
                "message": "Status tidak dapat diproses"
            })

        # 🔹 Insert tracking
        cursor.execute("""
            INSERT INTO tracking_pengiriman_elva
            (id_pengiriman_elva, status_tracking, keterangan_tracking)
            VALUES (%s, %s, %s)
        """, (id_pengiriman, new_status, ket))

        conn.commit()

        return jsonify({
            "status": "success",
            "new_status": new_status,
            "message": "Status berhasil diperbarui"
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()


@app.route('/api_status/<int:id>')
def api_status(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT status_pengiriman_elva
        FROM transaksi_elva
        WHERE id_transaksi_elva=%s
    """, (id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        return jsonify({"status_pengiriman_elva":"-"})

    return jsonify(data)

@app.route('/pesanan/<int:id_transaksi>')
def detail_pesanan_elva(id_transaksi):
    if 'user_online_elva' not in session:
        return redirect(url_for('login_elva'))

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            t.*,
            p.no_resi_elva,
            p.keterangan_elva
        FROM transaksi_elva t
        LEFT JOIN pengiriman_elva p
            ON p.id_transaksi_elva = t.id_transaksi_elva
        WHERE t.id_transaksi_elva=%s
        AND t.id_user_elva=%s
        AND t.tipe_elva='online'
    """, (id_transaksi, session['user_online_elva']))

    transaksi = cursor.fetchone()

    if not transaksi:
        flash('Pesanan tidak ditemukan', 'danger')
        return redirect(url_for('shop_online_elva'))
        
    qr_path = None
    if transaksi['kurir_elva'].lower().replace(' ', '_') == 'ambil_sendiri':
        qr_data = transaksi['no_faktur_elva']

        qr_folder = 'static/qr_elva'
        os.makedirs(qr_folder, exist_ok=True)

        qr_path = f"{qr_folder}/{qr_data}.png"

        if not os.path.exists(qr_path):
            qr_img = qrcode.make(qr_data)
            qr_img.save(qr_path)

    # 🔹 DETAIL ITEM
    cursor.execute("""
        SELECT d.*, o.nama_obat_elva
        FROM transaksi_detail_elva d
        JOIN obat_elva o ON o.id_obat_elva=d.id_obat_elva
        WHERE d.id_transaksi_elva=%s
    """, (id_transaksi,))
    items = cursor.fetchall()
    cursor.execute("""
        SELECT 
            tr.status_tracking,
            tr.keterangan_tracking,
            tr.waktu_tracking
        FROM tracking_pengiriman_elva tr
        JOIN pengiriman_elva p
            ON p.id_pengiriman_elva = tr.id_pengiriman_elva
        WHERE p.id_transaksi_elva=%s
        ORDER BY tr.waktu_tracking DESC
    """, (id_transaksi,))
    tracking = cursor.fetchall()


    cursor.close()
    conn.close()

    return render_template(
        'detail_pesanan_elva.html',
        transaksi=transaksi,
        items=items,
        qr_path=qr_path,
        tracking=tracking
    )
@app.route('/scan_qr_online_elva')
def scan_qr_online_elva():
    if 'nama_online_elva' not in session:
        return redirect(url_for('login_elva'))

    return render_template('scan_qr_online_elva.html')
@app.route('/proses_scan_online_elva', methods=['POST'])
def proses_scan_online_elva():

    if 'nama_online_elva' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"})

    data = request.get_json()
    no_faktur = data.get('no_faktur')

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_transaksi_elva, metode_bayar_elva,
               status_pembayaran_elva, kurir_elva
        FROM transaksi_elva
        WHERE no_faktur_elva=%s
        AND tipe_elva='online'
    """, (no_faktur,))

    trx = cursor.fetchone()

    if not trx:
        return jsonify({"status":"error","message":"Tidak ditemukan"})

    # 🔥 DANA
    # 🔥 DANA
    if trx['metode_bayar_elva'].lower() == 'dana':

        if trx['status_pembayaran_elva'] != 'lunas':

            cursor.execute("""
                UPDATE transaksi_elva
                SET status_pembayaran_elva='lunas'
                WHERE id_transaksi_elva=%s
            """,(trx['id_transaksi_elva'],))

            conn.commit()

        return jsonify({
            "status":"success",
            "message":"Pembayaran dikonfirmasi",
            "redirect": url_for('struk_online_elva',
                                id_transaksi=trx['id_transaksi_elva'])
        })

    # 💵 COD → LANGSUNG SELESAI
    if trx['metode_bayar_elva'].lower() == 'cod':

        cursor.execute("""
            UPDATE transaksi_elva
            SET status_pembayaran_elva='lunas',
                status_elva='selesai',
                status_pengiriman_elva='selesai',
                waktu_selesai_elva=NOW()
            WHERE id_transaksi_elva=%s
        """,(trx['id_transaksi_elva'],))

        conn.commit()

        return jsonify({
            "status":"success",
            "message":"Transaksi COD selesai",
            "redirect": url_for('struk_online_elva',
                                id_transaksi=trx['id_transaksi_elva'])
        })

    # DEFAULT (metode lain)
    return jsonify({
        "status":"success",
        "redirect": url_for('struk_online_elva',
                            id_transaksi=trx['id_transaksi_elva'])
    })
@app.route('/konfirmasi_ambil/<int:id>', methods=['POST'])
def konfirmasi_ambil(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("""
        UPDATE transaksi_elva
        SET status_elva='selesai',
            status_pembayaran_elva='lunas',
            status_pengiriman_elva='selesai',
            waktu_selesai_elva=%s
        WHERE id_transaksi_elva=%s
    """,(now, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('kasir_offline_elva'))
@app.route('/struk_online_elva/<int:id_transaksi>')
def struk_online_elva(id_transaksi):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM transaksi_elva
        WHERE id_transaksi_elva=%s
    """, (id_transaksi,))

    transaksi = cursor.fetchone()

    cursor.execute("""
        SELECT d.*, o.nama_obat_elva
        FROM transaksi_detail_elva d
        JOIN obat_elva o ON o.id_obat_elva=d.id_obat_elva
        WHERE d.id_transaksi_elva=%s
    """, (id_transaksi,))

    items = cursor.fetchall()

    # Update jadi LUNAS otomatis
    cursor.execute("""
        UPDATE transaksi_elva
        SET status_pembayaran_elva='lunas'
        WHERE id_transaksi_elva=%s
    """, (id_transaksi,))
    conn.commit()

    cursor.close()
    conn.close()

    return render_template(
        'struk_online_elva.html',
        transaksi=transaksi,
        items=items
    )
@app.route('/konfirmasi_bayar_online/<int:id>', methods=['POST'])
def konfirmasi_bayar_online(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # cek dulu
    cursor.execute("""
        SELECT status_pembayaran_elva 
        FROM transaksi_elva
        WHERE id_transaksi_elva=%s
    """,(id,))
    trx = cursor.fetchone()

    if not trx:
        return jsonify({"status":"error","message":"Data tidak ditemukan"})

    if trx['status_pembayaran_elva'] == 'lunas':
        return jsonify({"status":"error","message":"Sudah dibayar"})

    # update COD
    cursor.execute("""
        UPDATE transaksi_elva
        SET status_pembayaran_elva='lunas',
            status_elva='selesai',
            status_pengiriman_elva='selesai',
            waktu_selesai_elva=NOW()
        WHERE id_transaksi_elva=%s
    """,(id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status":"success"})
@app.route('/admin_gudang_elva')
@role_required(['admin', 'super_admin'])
def admin_gudang_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            g.id_gudang_elva,
            g.nama_gudang_elva,
            IFNULL(SUM(o.stok_elva),0) AS total_stok
        FROM gudang_elva g
        LEFT JOIN obat_elva o 
            ON g.id_gudang_elva = o.id_gudang_elva
        GROUP BY g.id_gudang_elva, g.nama_gudang_elva
        ORDER BY g.id_gudang_elva DESC
    """)

    gudang = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_gudang_elva.html', gudang=gudang)

@app.route('/detail_gudang_elva/<int:id>')
@role_required(['admin', 'super_admin'])
def detail_gudang_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.id_obat_elva,
            o.kode_obat_elva,
            o.nama_obat_elva,
            o.stok_elva,
            o.harga_elva,
            k.nama_kategori_elva,
            g.nama_gudang_elva
        FROM obat_elva o
        JOIN gudang_elva g 
            ON o.id_gudang_elva = g.id_gudang_elva
        LEFT JOIN kategori_elva k
            ON o.kategori_id_elva = k.id_kategori_elva
        WHERE g.id_gudang_elva = %s
        ORDER BY o.nama_obat_elva ASC
    """,(id,))

    obat = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'detail_gudang_elva.html',
        obat=obat
    )

@app.route('/tambah_gudang_elva', methods=['POST'])
@role_required(['admin','super_admin'])
def tambah_gudang_elva():

    nama = request.form['nama_gudang_elva']

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO gudang_elva (nama_gudang_elva)
        VALUES (%s)
    """,(nama,))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Gudang berhasil ditambahkan','success')
    return redirect(url_for('admin_gudang_elva'))

@app.route('/edit_gudang_elva/<int:id>', methods=['POST'])
@role_required(['admin','super_admin'])
def edit_gudang_elva(id):

    nama = request.form['nama_gudang_elva']

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE gudang_elva
        SET nama_gudang_elva=%s
        WHERE id_gudang_elva=%s
    """,(nama,id))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Gudang berhasil diupdate','success')
    return redirect(url_for('admin_gudang_elva'))

@app.route('/hapus_gudang_elva/<int:id>')
@role_required(['admin','super_admin'])
def hapus_gudang_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM gudang_elva WHERE id_gudang_elva=%s",(id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Gudang berhasil dihapus','danger')
    return redirect(url_for('admin_gudang_elva'))
@app.route('/admin_peracik_elva')
@role_required(['admin', 'super_admin'])
def admin_peracik_elva():
    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
    r.no_resep_elva,
    p.nama_lengkap_elva,
    d.nama_dokter_elva,
    t.no_faktur_elva,

    COALESCE(rc.nama_obat_elva, a.nama_obat_elva) AS nama_obat,

    rd.jenis_obat_elva,
    rd.dosis_elva,
    rd.jumlah_elva,
    rd.catatan_elva

FROM resep_elva r

LEFT JOIN pasien_elva p 
    ON r.id_pasien_elva = p.id_pasien_elva

LEFT JOIN dokter_elva d 
    ON r.id_dokter_elva = d.id_dokter_elva

LEFT JOIN transaksi_elva t 
    ON r.id_transaksi_elva = t.id_transaksi_elva

LEFT JOIN resep_detail_elva rd 
    ON r.id_resep_elva = rd.id_resep_elva

LEFT JOIN racikan_elva rc 
    ON rc.id_racikan_elva = rd.id_racikan_elva

LEFT JOIN obat_elva a 
    ON a.id_obat_elva = rd.id_obat_elva

    """)

    peracik = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_peracik_elva.html', peracik=peracik)



@app.route('/hapus_resep_elva/<int:id>')
@role_required(['admin','super_admin'])
def hapus_resep_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM resep_elva WHERE id_resep_elva=%s",(id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Resep berhasil dihapus','danger')
    return redirect(url_for('admin_resep_obat_elva'))

@app.route('/tambah_detail_resep_elva', methods=['POST'])
@role_required(['admin','super_admin'])
def tambah_detail_resep_elva():

    id_resep = request.form['id_resep_elva']
    id_obat = request.form['id_obat_elva']
    dosis = request.form['dosis_elva']
    jumlah = request.form['jumlah_elva']

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resep_detail_elva
        (id_resep_elva,id_obat_elva,dosis_elva,jumlah_elva)
        VALUES (%s,%s,%s,%s)
    """,(id_resep,id_obat,dosis,jumlah))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Detail resep berhasil ditambahkan','success')
    return redirect(url_for('admin_resep_obat_elva'))

@app.route('/tambah_racikan_elva', methods=['POST'])
@role_required(['admin','super_admin'])
def tambah_racikan_elva():

    id_resep = request.form['id_resep_elva']
    id_peracik = request.form['id_peracik_elva']
    catatan = request.form['catatan_elva']

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO racikan_elva
        (id_resep_elva,id_peracik_elva,catatan_elva)
        VALUES (%s,%s,%s)
    """,(id_resep,id_peracik,catatan))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Racikan berhasil ditambahkan','success')
    return redirect(url_for('admin_resep_obat_elva'))
@app.route('/detail_resep_elva/<int:id>')
@role_required(['admin', 'super_admin'])
def detail_resep_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    try:
        # ================= HEADER RESEP =================
        cursor.execute("""
            SELECT 
                r.id_resep_elva,
                r.no_resep_elva,
                r.tipe_elva,
                r.status_elva,
                p.nama_pasien_elva,
                d.nama_elva AS nama_dokter
            FROM resep_elva r
            LEFT JOIN pasien_elva p 
                ON r.id_pasien_elva = p.id_pasien_elva
            LEFT JOIN users_elva d 
                ON r.id_dokter_elva = d.id_user_elva
            WHERE r.id_resep_elva = %s
        """, (id,))
        
        resep = cursor.fetchone()

        if not resep:
            return "Resep tidak ditemukan", 404

        # ================= DETAIL OBAT =================
        cursor.execute("""
            SELECT 
                rd.id_detail_elva,
                rd.jumlah_elva,
                rd.dosis_elva,
                o.nama_obat_elva,
                o.harga_elva,
                (rd.jumlah_elva * o.harga_elva) AS subtotal_elva
            FROM resep_detail_elva rd
            INNER JOIN obat_elva o 
                ON rd.id_obat_elva = o.id_obat_elva
            WHERE rd.id_resep_elva = %s
        """, (id,))
        
        detail = cursor.fetchall()
        # ambil semua obat untuk dropdown
        cursor.execute("SELECT * FROM obat_elva ORDER BY nama_obat_elva ASC")
        obat_list = cursor.fetchall()

        # ================= TOTAL =================
        total = 0
        for item in detail:
            subtotal = item.get('subtotal_elva') or 0
            total += float(subtotal)

        return render_template(
            "detail_resep_elva.html",
            resep=resep,
            detail=detail,
            total=total,
            obat_list=obat_list
        )

    finally:
        cursor.close()
        conn.close()
@app.route('/edit_detail_resep_elva/<int:id>', methods=['GET','POST'])
@role_required(['admin','super_admin'])
def edit_detail_resep_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        dosis = request.form['dosis_elva']
        jumlah = request.form['jumlah_elva']

        cursor.execute("""
            UPDATE resep_detail_elva
            SET dosis_elva=%s, jumlah_elva=%s
            WHERE id_detail_elva=%s
        """,(dosis,jumlah,id))

        conn.commit()
        flash('Detail berhasil diupdate','success')
        return redirect(request.referrer)

    cursor.execute("SELECT * FROM resep_detail_elva WHERE id_detail_elva=%s",(id,))
    detail = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit_detail_resep_elva.html', detail=detail)
@app.route('/hapus_detail_resep_elva/<int:id>')
@role_required(['admin','super_admin'])
def hapus_detail_resep_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM resep_detail_elva WHERE id_detail_elva=%s",(id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Detail resep berhasil dihapus','danger')
    return redirect(request.referrer)

# ===============================
# HALAMAN KASIR OFFLINE
# ===============================
@app.route('/kasir_offline_elva')
@role_required(['kasir'])
def kasir_offline_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # ================= MASTER DATA =================
    cursor.execute("SELECT * FROM pasien_elva ORDER BY nama_lengkap_elva ASC")
    pasien = cursor.fetchall()

    cursor.execute("SELECT * FROM obat_elva")
    obat = cursor.fetchall()

    cursor.execute("SELECT id_dokter_elva, nama_dokter_elva FROM dokter_elva")
    dokter = cursor.fetchall()

    cursor.execute("SELECT * FROM gudang_elva")
    gudang = cursor.fetchall()

    cursor.execute("""
    SELECT 
        t.id_transaksi_elva,
        t.no_faktur_elva,
        t.total_elva,
        t.status_elva,
        t.status_verifikasi_elva,
        t.kurir_elva,
        t.tanggal_elva,
        u.nama_elva
    FROM transaksi_elva t
    LEFT JOIN users_elva u ON t.id_user_elva = u.id_user_elva
    WHERE t.kurir_elva = 'Ambil Sendiri'
    AND t.status_elva != 'selesai'
    AND t.status_verifikasi_elva != 'lunas'
    ORDER BY t.tanggal_elva DESC
    """)
    pesanan_online = cursor.fetchall()

    cursor.close()
    conn.close()

    keranjang = session.get('keranjang_elva', [])
    grand_total = sum(item['total'] for item in keranjang)

    return render_template(
        'kasir_offline_elva.html',
        pasien=pasien,
        obat=obat,
        dokter=dokter,
        gudang=gudang,
        keranjang=keranjang,
        grand_total=grand_total,
        pesanan_online=pesanan_online,  # 🔥 KIRIM KE HTML
        today=datetime.now().strftime("%Y-%m-%d")
    )
@app.route('/verifikasi_pesanan_elva/<int:id>', methods=['POST'])
@role_required(['kasir'])
def verifikasi_pesanan_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    try:
        # 🔍 Ambil data transaksi
        cursor.execute("""
            SELECT kurir_elva
            FROM transaksi_elva
            WHERE id_transaksi_elva = %s
        """, (id,))
        transaksi = cursor.fetchone()

        if not transaksi:
            flash("Transaksi tidak ditemukan!", "danger")
            return redirect(url_for('kasir_offline_elva'))

        # ❌ VALIDASI: kasir hanya boleh ambil sendiri
        if transaksi['kurir_elva'] != 'Ambil Sendiri':
            flash("Verifikasi untuk pengiriman hanya bisa dilakukan admin!", "warning")
            return redirect(url_for('kasir_offline_elva'))

        # ✅ UPDATE
        cursor.execute("""
            UPDATE transaksi_elva
            SET 
                status_verifikasi_elva = 'sudah',
                status_elva = 'diproses'
            WHERE id_transaksi_elva = %s
        """, (id,))

        conn.commit()
        flash("Pesanan berhasil diverifikasi!", "success")

    except Exception as e:
        conn.rollback()
        flash(str(e), "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('kasir_offline_elva'))
@app.route('/verifikasi_admin_elva/<int:id>', methods=['POST'])
@role_required(['admin'])
def verifikasi_admin_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT kurir_elva
            FROM transaksi_elva
            WHERE id_transaksi_elva = %s
        """, (id,))
        transaksi = cursor.fetchone()

        if not transaksi:
            flash("Transaksi tidak ditemukan!", "danger")
            return redirect(url_for('admin_dashboard'))

        # ❌ ADMIN hanya untuk pengiriman
        if transaksi['kurir_elva'] == 'Ambil Sendiri':
            flash("Pesanan ambil sendiri diverifikasi kasir!", "warning")
            return redirect(url_for('admin_dashboard'))

        cursor.execute("""
            UPDATE transaksi_elva
            SET 
                status_verifikasi_elva = 'sudah',
                status_elva = 'diproses'
            WHERE id_transaksi_elva = %s
        """, (id,))

        conn.commit()
        flash("Pesanan pengiriman berhasil diverifikasi!", "success")

    except Exception as e:
        conn.rollback()
        flash(str(e), "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))
@app.route('/konfirmasi_ambil_elva/<int:id>', methods=['POST'])
@role_required(['kasir'])
def konfirmasi_ambil_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE transaksi_elva
            SET 
                status_elva = 'selesai',
                status_pengiriman_elva = 'selesai',
                status_verifikasi_elva = 'lunas',
                waktu_selesai_elva = NOW()
            WHERE id_transaksi_elva = %s
        """, (id,))
        cursor.execute("""
            UPDATE pengiriman_elva
            SET 
                status_elva = 'sampai',
                       keterangan_elva = 'Diambil sendiri oleh pelanggan'
            WHERE id_transaksi_elva = %s
        """, (id,))

        conn.commit()

        # 🔥 LANGSUNG KE STRUK
        return redirect(url_for('struk_kasir_elva', id=id))

    except Exception as e:
        conn.rollback()
        flash(str(e), "danger")
        return redirect(url_for('kasir_offline_elva'))

    finally:
        cursor.close()
        conn.close()
@app.route('/tambah_pasien_elva', methods=['GET', 'POST'])
def tambah_pasien_elva():
    if request.method == 'POST':
        # Ambil data dari form (sesuai HTML baru)
        nama_lengkap = request.form['nama_lengkap']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        no_telepon = request.form.get('no_telepon')  # optional
        alergi = request.form.get('alergi')          # optional
        catatan_khusus = request.form.get('catatan_khusus')  # optional

        # Masukkan data ke database
        conn = get_db_connection_elva()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pasien_elva (
                nama_lengkap_elva, tanggal_lahir_elva, jenis_kelamin_elva, 
                alamat_elva, no_telepon_elva, alergi_elva, catatan_khusus_elva
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            nama_lengkap, 
            tanggal_lahir, 
            jenis_kelamin, 
            alamat, 
            no_telepon, 
            alergi, 
            catatan_khusus
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Pasien berhasil ditambahkan", "success")
        return redirect(url_for('kasir_offline_elva'))

    return render_template('tambah_pasien_elva.html')
@app.route('/tambah_dokter_elva', methods=['GET', 'POST'])
def tambah_dokter_elva():
    if request.method == 'POST':
        # Ambil data dari form
        nama_dokter = request.form['nama_dokter']
        spesialis = request.form['spesialis']
        alamat = request.form['alamat']
        kota = request.form['kota']
        no_tlp = request.form['no_tlp']

        # Masukkan data ke dalam database
        conn = get_db_connection_elva()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dokter_elva (
                nama_dokter_elva, spesialis_elva, alamat, kota_elva, no_tlp_elva
            ) VALUES (%s, %s, %s, %s, %s)
        """, (nama_dokter, spesialis, alamat, kota, no_tlp))
        
        conn.commit()
        cursor.close()
        conn.close()

        flash("Dokter berhasil ditambahkan", "success")
        return redirect(url_for('kasir_offline_elva'))

    return render_template('tambah_dokter_elva.html')
@app.route('/pilih_obat_elva')
def pilih_obat_elva():

    search = request.args.get('search', '')
    kategori = request.args.get('kategori', '')

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT o.*, k.nama_kategori_elva
    FROM obat_elva o
    JOIN kategori_elva k 
    ON o.kategori_id_elva = k.id_kategori_elva
    WHERE 1=1
    """
    params = []

    # 🔍 SEARCH
    if search:
        query += " AND o.nama_obat_elva LIKE %s"
        params.append(f"%{search}%")

    # 🔽 FILTER KATEGORI
    if kategori:
        query += " AND o.kategori_id_elva = %s"
        params.append(kategori)

    cursor.execute(query, params)
    obat_list = cursor.fetchall()

    # ambil kategori
    cursor.execute("SELECT * FROM kategori_elva")
    kategori_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'pilih_obat_elva.html',
        obat_list=obat_list,
        kategori_list=kategori_list,
        search=search,
        kategori=kategori
    )
@app.route('/tambah_obat_ke_keranjang', methods=['POST'])
@role_required(['kasir'])
def tambah_obat_ke_keranjang():

    # =============================
    # Ambil data dari JSON / Form
    # =============================
    if request.is_json:
        data = request.get_json()
        obat_ids = data.get('obat_ids', [])

        # fallback jika kirim single
        if not obat_ids and data.get('obat_id'):
            obat_ids = [data.get('obat_id')]
    else:
        obat_ids = request.form.getlist('obat_ids[]')
        if not obat_ids:
            single = request.form.get('obat_id')
            if single:
                obat_ids = [single]

    if not obat_ids:
        return jsonify({"status": "error", "message": "ID kosong"}), 400


    # =============================
    # Ambil keranjang dari session
    # =============================
    keranjang = session.get('keranjang_elva', [])


    # =============================
    # Loop setiap obat
    # =============================
    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    for obat_id in obat_ids:

        cursor.execute(
            "SELECT * FROM obat_elva WHERE id_obat_elva=%s",
            (obat_id,)
        )
        obat = cursor.fetchone()

        if not obat:
            continue

        harga = float(obat['harga_elva'])

        # cek apakah sudah ada (merge qty)
        existing = next(
            (item for item in keranjang
             if item['ref_id'] == obat['id_obat_elva']
             and item['tipe'] == 'obat'),
            None
        )

        if existing:
            existing['jumlah'] += 1
            existing['total'] = existing['jumlah'] * existing['harga']
        else:
            keranjang.append({
                "uid": f"obat_{obat['id_obat_elva']}",
                "ref_id": obat['id_obat_elva'],
                "tipe": "obat",
                "nama": obat['nama_obat_elva'],
                "jenis_obat_elva": obat['jenis_obat_elva'],
                "harga": harga,
                "jumlah": 1,
                "total": harga
            })

    cursor.close()
    conn.close()


    # =============================
    # Simpan kembali ke session
    # =============================
    session['keranjang_elva'] = keranjang
    session.modified = True


    # =============================
    # Hitung grand total
    # =============================
    grand_total = sum(float(item['total']) for item in keranjang)


    # =============================
    # Response AJAX
    # =============================
    return jsonify({
        "status": "success",
        "jumlah_item": len(keranjang),
        "grand_total": grand_total,
        "keranjang": keranjang
    })
@app.route('/update_qty', methods=['POST'])
@role_required(['kasir'])
def update_qty():

    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    uid = data.get('uid')
    qty = data.get('qty')

    if not uid or qty is None:
        return jsonify({"status": "error", "message": "Data tidak lengkap"}), 400

    try:
        qty = int(qty)
        if qty < 1:
            qty = 1
    except:
        return jsonify({"status": "error", "message": "Qty tidak valid"}), 400

    keranjang = session.get('keranjang_elva', [])

    found = False

    for item in keranjang:
        if item['uid'] == uid:
            item['jumlah'] = qty
            item['total'] = qty * item['harga']
            found = True
            break

    if not found:
        return jsonify({"status": "error", "message": "Item tidak ditemukan"}), 404

    session['keranjang_elva'] = keranjang
    session.modified = True

    grand_total = sum(i['total'] for i in keranjang)

    return jsonify({
        "status": "success",
        "grand_total": grand_total
    })

@app.route('/remove_item', methods=['POST'])
@role_required(['kasir'])
def remove_item():

    data = request.get_json()
    uid = data.get('uid')

    keranjang = session.get('keranjang_elva', [])
    keranjang = [i for i in keranjang if i['uid'] != uid]

    session['keranjang_elva'] = keranjang
    session.modified = True

    return jsonify({
        "status": "success",
        "keranjang": keranjang,
        "grand_total": sum(i['total'] for i in keranjang)
    })
@app.route('/tambah_racikan_elva_kasir', methods=['GET', 'POST'])
@role_required(['kasir'])
def tambah_racikan_elva_kasir():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        nama_obat = request.form.get('nama_obat')
        dosis = request.form.get('dosis')
        catatan = request.form.get('catatan')

        cursor.execute('''
            INSERT INTO racikan_elva (nama_obat_elva, dosis_elva, catatan_elva)
            VALUES (%s, %s, %s)
        ''', (nama_obat, dosis, catatan))

        conn.commit()

        return redirect(url_for('tambah_racikan_elva_kasir'))

    cursor.execute("SELECT * FROM racikan_elva")
    racikan_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'tambah_racikan_elva.html',
        racikan_list=racikan_list
    )

@app.route('/add_to_cart_racikan', methods=['POST'])
@role_required(['kasir'])
def add_to_cart_racikan():

    data = request.get_json()
    racikan_ids = data.get('racikan_ids', [])

    if not racikan_ids:
        return jsonify({"status": "error", "message": "Tidak ada racikan dipilih"})

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    keranjang = session.get('keranjang_elva', [])
    harga_racikan = 10000

    for racikan_id in racikan_ids:

        cursor.execute(
            "SELECT * FROM racikan_elva WHERE id_racikan_elva=%s",
            (racikan_id,)
        )
        racikan = cursor.fetchone()

        if not racikan:
            continue

        existing = next(
            (item for item in keranjang
             if item['ref_id'] == racikan['id_racikan_elva']
             and item['tipe'] == 'racikan'),
            None
        )

        if existing:
            existing['jumlah'] += 1
            existing['total'] = existing['jumlah'] * existing['harga']
        else:
            keranjang.append({
                "uid": f"racikan_{racikan['id_racikan_elva']}",
                "ref_id": racikan['id_racikan_elva'],
                "tipe": "racikan",
                "nama": racikan['nama_obat_elva'],
                "jenis_obat_elva": "Racikan",
                "harga": harga_racikan,
                "jumlah": 1,
                "total": harga_racikan
            })

    cursor.close()
    conn.close()

    session['keranjang_elva'] = keranjang
    session.modified = True

    return jsonify({
        "status": "success",
        "keranjang": keranjang,
        "grand_total": sum(i['total'] for i in keranjang)
    })



@app.route('/generate_resep')
def generate_resep():
    # Logika untuk menghasilkan nomor resep, misalnya dengan menambahkan angka acak
    no_resep = f"{random.randint(1, 999):03d}"  # Misal format: 001, 002, dst.
    
    return jsonify({
        "status": "success",
        "no_resep": no_resep
    })
@app.route('/proses_bayar_kasir_elva', methods=['POST'])
@role_required(['kasir'])
def proses_bayar_kasir_elva():

    # ================= VALIDASI =================
    if not session.get('keranjang_elva'):
        flash("Keranjang kosong", "danger")
        return redirect(url_for('kasir_offline_elva'))

    data_pasien = session.get('data_pasien')
    if not data_pasien:
        flash("Pasien belum dipilih!", "danger")
        return redirect(url_for('kasir_offline_elva'))

    metode_bayar = request.form.get('metode_bayar_elva')
    if not metode_bayar:
        flash("Metode bayar belum dipilih!", "danger")
        return redirect(url_for('kasir_offline_elva'))

    # ================= AMBIL DATA =================
    keranjang = session['keranjang_elva']

    id_pasien = data_pasien.get('id_pasien')
    id_dokter = data_pasien.get('id_dokter')
    no_resep = data_pasien.get('no_resep')
    id_user = session.get('user_id_elva')

    # ================= VALIDASI ITEM =================
    for item in keranjang:
        if 'jumlah' not in item or 'harga' not in item or 'total' not in item:
            flash("Data keranjang tidak valid!", "danger")
            return redirect(url_for('kasir_offline_elva'))

    # ================= HITUNG TOTAL =================
    subtotal = sum(i['total'] for i in keranjang)
    diskon = subtotal * 0.05 if subtotal > 50000 else 0
    pajak = (subtotal - diskon) * 0.03
    total_transaksi = subtotal - diskon + pajak

    no_faktur = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    try:
        # ================= INSERT TRANSAKSI =================
        cursor.execute("""
            INSERT INTO transaksi_elva
            (no_faktur_elva, tanggal_elva, id_user_elva, id_pasien_elva,
             metode_bayar_elva, total_elva,
             tipe_elva, status_elva, status_pengiriman_elva, waktu_selesai_elva)
            VALUES (%s,%s,%s,%s,%s,%s,'offline','selesai','selesai',%s)
        """, (
            no_faktur,
            datetime.now(),
            id_user,
            id_pasien,
            metode_bayar,
            total_transaksi,
            datetime.now()
        ))

        id_transaksi = cursor.lastrowid

        # ================= INSERT DETAIL TRANSAKSI =================
        for item in keranjang:
            id_obat = item['ref_id'] if item['tipe'] == 'obat' else None
            id_racikan = item['ref_id'] if item['tipe'] == 'racikan' else None

            cursor.execute("""
                INSERT INTO transaksi_detail_elva
                (id_transaksi_elva, id_obat_elva, id_racikan_elva,
                 jumlah_elva, harga_elva, diskon_elva, total_elva)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                id_transaksi,
                id_obat,
                id_racikan,
                item['jumlah'],
                item['harga'],
                0,
                item['total']
            ))

        # ================= INSERT RESEP =================
        if no_resep and id_dokter:

            # cek duplikat
            cursor.execute("""
                SELECT id_resep_elva 
                FROM resep_elva 
                WHERE no_resep_elva = %s
            """, (no_resep,))
            if cursor.fetchone():
                raise Exception("No resep sudah digunakan!")

            cursor.execute("""
                INSERT INTO resep_elva
                (no_resep_elva, id_pasien_elva, id_dokter_elva,
                 id_transaksi_elva, tanggal_resep_elva)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                no_resep,
                id_pasien,
                id_dokter,
                id_transaksi,
                datetime.now()
            ))

            id_resep = cursor.lastrowid

            # ================= AMBIL DATA RACIKAN (OPTIMASI) =================
            racikan_ids = [i['ref_id'] for i in keranjang if i['tipe'] == 'racikan']
            racikan_map = {}

            if racikan_ids:
                format_strings = ','.join(['%s'] * len(racikan_ids))
                cursor.execute(f"""
                    SELECT id_racikan_elva, dosis_elva, catatan_elva
                    FROM racikan_elva
                    WHERE id_racikan_elva IN ({format_strings})
                """, tuple(racikan_ids))

                racikan_map = {
                    r['id_racikan_elva']: r
                    for r in cursor.fetchall()
                }

            # ================= INSERT RESEP DETAIL =================
            for item in keranjang:

                id_obat = item['ref_id'] if item['tipe'] == 'obat' else None
                id_racikan = item['ref_id'] if item['tipe'] == 'racikan' else None

                jenis_obat = (
                    item.get('jenis_obat_elva')
                    or ('racikan' if id_racikan else 'obat')
                )

                # 🔥 LOGIC DOSIS & CATATAN
                if id_racikan:
                    racikan_data = racikan_map.get(id_racikan)
                    dosis = racikan_data['dosis_elva'] if racikan_data else '-'
                    catatan = racikan_data['catatan_elva'] if racikan_data else '-'
                else:
                    dosis = '-'
                    catatan = '-'

                cursor.execute("""
                    INSERT INTO resep_detail_elva
                    (id_resep_elva, id_obat_elva, id_racikan_elva,
                     jenis_obat_elva, dosis_elva, jumlah_elva, catatan_elva)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (
                    id_resep,
                    id_obat,
                    id_racikan,
                    jenis_obat,
                    dosis,
                    item['jumlah'],
                    catatan
                ))

        conn.commit()

        # ================= AMBIL DATA STRUK =================
        cursor.execute("""
            SELECT 
                t.*,
                p.nama_lengkap_elva,
                d.nama_dokter_elva,
                r.no_resep_elva
            FROM transaksi_elva t
            LEFT JOIN pasien_elva p ON t.id_pasien_elva = p.id_pasien_elva
            LEFT JOIN resep_elva r ON t.id_transaksi_elva = r.id_transaksi_elva
            LEFT JOIN dokter_elva d ON r.id_dokter_elva = d.id_dokter_elva
            WHERE t.id_transaksi_elva=%s
        """, (id_transaksi,))
        transaksi_pdf = cursor.fetchone()

        cursor.execute("""
            SELECT 
                td.jumlah_elva,
                td.harga_elva,
                td.total_elva,
                CASE 
                    WHEN td.id_racikan_elva IS NOT NULL THEN rc.nama_obat_elva
                    ELSE o.nama_obat_elva
                END AS nama_tampil,
                CASE 
                    WHEN td.id_racikan_elva IS NOT NULL THEN 'Racikan'
                    ELSE o.jenis_obat_elva
                END AS jenis_tampil,
                rc.dosis_elva,
                rc.catatan_elva,
                CASE 
                    WHEN td.id_racikan_elva IS NOT NULL THEN 1
                    ELSE 0
                END AS is_racikan
            FROM transaksi_detail_elva td
            LEFT JOIN obat_elva o ON td.id_obat_elva = o.id_obat_elva
            LEFT JOIN racikan_elva rc ON td.id_racikan_elva = rc.id_racikan_elva
            WHERE td.id_transaksi_elva=%s
        """, (id_transaksi,))
        detail_pdf = cursor.fetchall()

        # ================= GENERATE PDF =================
        generate_struk_pdf(transaksi_pdf, detail_pdf)

    except Exception as e:
        conn.rollback()
        flash(str(e), "danger")
        return redirect(url_for('kasir_offline_elva'))

    finally:
        cursor.close()
        conn.close()

    # ================= CLEAR SESSION =================
    session.pop('keranjang_elva', None)
    session.pop('data_pasien', None)

    return redirect(url_for('struk_kasir_elva', id=id_transaksi))

@app.route('/struk_kasir_elva/<int:id>')
@role_required(['kasir'])
def struk_kasir_elva(id):

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            t.*,
            p.nama_lengkap_elva,
            d.nama_dokter_elva,
            r.no_resep_elva
        FROM transaksi_elva t
        LEFT JOIN pasien_elva p
            ON t.id_pasien_elva = p.id_pasien_elva
        LEFT JOIN resep_elva r
            ON t.id_transaksi_elva = r.id_transaksi_elva
        LEFT JOIN dokter_elva d
            ON r.id_dokter_elva = d.id_dokter_elva
        WHERE t.id_transaksi_elva=%s
    """, (id,))

    transaksi = cursor.fetchone()

    cursor.execute("""
        SELECT 
            td.jumlah_elva,
            td.harga_elva,
            td.total_elva,

            -- Nama tampil
            CASE 
                WHEN td.id_racikan_elva IS NOT NULL 
                    THEN rc.nama_obat_elva
                ELSE o.nama_obat_elva
            END AS nama_tampil,

            -- Jenis tampil
            CASE 
                WHEN td.id_racikan_elva IS NOT NULL 
                    THEN 'Racikan'
                ELSE o.jenis_obat_elva
            END AS jenis_tampil,

            rc.dosis_elva,
            rc.catatan_elva,

            CASE 
                WHEN td.id_racikan_elva IS NOT NULL 
                    THEN 1
                ELSE 0
            END AS is_racikan

        FROM transaksi_detail_elva td

        LEFT JOIN obat_elva o
            ON td.id_obat_elva = o.id_obat_elva

        LEFT JOIN racikan_elva rc
            ON td.id_racikan_elva = rc.id_racikan_elva

        WHERE td.id_transaksi_elva=%s
    """, (id,))

    detail = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "struk_kasir_elva.html",
        transaksi=transaksi,
        detail=detail
    )


# ===============================
# RESET KERANJANG
# ===============================
@app.route('/reset_kasir_elva')
@role_required(['kasir'])
def reset_kasir_elva():
    session.pop('keranjang_elva', None)
    flash("Keranjang dikosongkan", "info")
    return redirect(url_for('kasir_offline_elva'))

@app.route('/checkout_kasir_elva', methods=['POST'])
@role_required(['kasir'])
def checkout_kasir_elva():

    keranjang = session.get('keranjang_elva', [])

    if not keranjang:
        flash("Keranjang kosong", "danger")
        return redirect(url_for('kasir_offline_elva'))

    # =========================
    # AMBIL ID DARI FORM
    # =========================
    id_pasien = request.form.get("id_pasien_elva")
    id_dokter = request.form.get("dokter_elva")
    no_resep = request.form.get("no_resep_elva")

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    # =========================
    # AMBIL NAMA PASIEN
    # =========================
    cursor.execute(
        "SELECT nama_lengkap_elva FROM pasien_elva WHERE id_pasien_elva=%s",
        (id_pasien,)
    )
    pasien = cursor.fetchone()

    # =========================
    # AMBIL NAMA DOKTER
    # =========================
    cursor.execute(
        "SELECT nama_dokter_elva FROM dokter_elva WHERE id_dokter_elva=%s",
        (id_dokter,)
    )
    dokter = cursor.fetchone()

    cursor.close()
    conn.close()

    nama_pasien = pasien['nama_lengkap_elva'] if pasien else "-"
    nama_dokter = dokter['nama_dokter_elva'] if dokter else "-"

    # =========================
    # SIMPAN KE SESSION
    # =========================
    session['data_pasien'] = {
        "id_pasien": id_pasien,
        "id_dokter": id_dokter,   # 🔥 tambahkan ini
        "nama_pasien": nama_pasien,
        "nama_dokter": nama_dokter,
        "no_resep": no_resep
    }


    # =========================
    # HITUNG TOTAL
    # =========================
    subtotal = sum(i['total'] for i in keranjang)

    diskon = subtotal * 0.05 if subtotal > 50000 else 0
    pajak = (subtotal - diskon) * 0.03
    grand_total = subtotal - diskon + pajak

    no_faktur = "OFF-" + datetime.now().strftime("%Y%m%d%H%M%S")

    return render_template(
        "checkout_kasir_elva.html",
        keranjang=keranjang,
        subtotal=subtotal,
        diskon=diskon,
        pajak=pajak,
        grand_total=grand_total,
        no_faktur=no_faktur,
        no_resep=no_resep,
        nama_pasien=nama_pasien,
        nama_dokter=nama_dokter,
        id_pasien=id_pasien,
        kasir=session.get("nama_elva") or session.get("nama_online_elva"),
        today=datetime.now().strftime("%Y-%m-%d"),
        waktu=datetime.now().strftime("%H:%M:%S")
    )


@app.route('/kurir_dashboard_elva')
@role_required(['kurir'])
def kurir_dashboard_elva():

    conn = get_db_connection_elva()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            pg.id_pengiriman_elva,
            pg.no_resi_elva,
            pg.status_elva,
            t.no_faktur_elva,
            t.alamat_elva,
            t.total_elva
        FROM pengiriman_elva pg
        JOIN transaksi_elva t 
            ON t.id_transaksi_elva = pg.id_transaksi_elva
        WHERE pg.status_elva != 'sampai'
        ORDER BY pg.id_pengiriman_elva DESC
    """)

    paket = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) as total
        FROM pengiriman_elva
        WHERE status_elva != 'sampai'
    """)
    total = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template(
        'kurir_dashboard_elva.html',
        paket=paket,
        total=total
    )


# ================== LOGOUT ==================
@app.route('/logout_elva')
def logout_elva():
    session.clear()
    return redirect(url_for('login_elva'))
