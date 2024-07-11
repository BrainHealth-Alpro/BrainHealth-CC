from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    return db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nomor_telepon = db.Column(db.String(20), unique=True, nullable=False)
    foto_profil = db.Column(db.Text, nullable=True)
    tempat_lahir = db.Column(db.Text, nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=True)
    kata_sandi = db.Column(db.Text, nullable=False)
    tipe = db.Column(db.String(6), nullable=False) # dokter | pasien
    riwayat = db.relationship('Riwayat', backref='user', lazy=True)

    def __repr__(self):
        return '<User id=%r nama_lengkap=%r email=%r nomor_telepon=%r foto_profil=%r tempat_lahir=%r tanggal_lahir=%r kata_sandi=%r tipe=%r>' % (self.id, self.nama_lengkap, self.email, self.nomor_telepon, self.foto_profil, self.tempat_lahir, self.tanggal_lahir, self.kata_sandi, self.tipe)
    
    def set_password(self, kata_sandi):
        self.kata_sandi = generate_password_hash(kata_sandi)

    def check_password(self, kata_sandi):
        return check_password_hash(self.kata_sandi, kata_sandi)


class Tumor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(16), unique=True, nullable=False)
    perawatan = db.Column(db.Text, nullable=False)
    riwayat = db.relationship('Riwayat', backref='tumor', lazy=True)

    def __repr__(self):
        return '<Tumor id=%r nama=%r perawatan=%r>' % (self.id, self.nama, self.perawatan)


class Riwayat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap_pasien = db.Column(db.String(80), nullable=False)
    hasil = db.Column(db.String(30), nullable=False) # Tidak ada tumor | Terdapat tumor terdeteksi
    datetime = db.Column(db.DateTime, nullable=False)
    gambar = db.Column(db.Text, nullable=False) # bisa hyperlink atau internal path ke file
    tumor_id = db.Column(db.Integer, db.ForeignKey('tumor.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Riwayat id=%r nama_lengkap_pasien=%r hasil=%r tanggal=%r waktu=%r gambar=%r tumor_id=%r user_id=%r>' % (self.id, self.nama_lengkap_pasien, self.hasil, self.tanggal, self.waktu, self.gambar, self.tumor_id, self.user_id)