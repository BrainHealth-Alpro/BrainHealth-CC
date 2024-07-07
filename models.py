from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nomor_telepon = db.Column(db.String(20), unique=True, nullable=False)
    kata_sandi = db.Column(db.String(64), nullable=False)
    tipe = db.Column(db.String(6), nullable=False) # dokter | pasien
    riwayat = db.relationship('Riwayat', backref='user', lazy=True)

    def __repr__(self):
        return '<User id=%r nama_lengkap=%r email=%r nomor_telepon=%r kata_sandi=%r tipe=%r>' % self.id, self.nama_lengkap, self.email, self.nomor_telepon, self.kata_sandi, self.tipe


class Tumor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(16), unique=True, nullable=False)
    perawatan = db.Column(db.Text, nullable=False)
    riwayat = db.relationship('Riwayat', backref='tumor', lazy=True)

    def __repr__(self):
        return '<Tumor id=%r nama=%r perawatan=%r>' % self.id, self.nama, self.perawatan


class Riwayat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap_pasien = db.Column(db.String(80), nullable=False)
    hasil = db.Column(db.String(30), nullable=False) # Tidak ada tumor | Terdapat tumor terdeteksi
    tanggal = db.Column(db.Date, nullable=False)
    waktu = db.Column(db.Time, nullable=False)
    gambar = db.Column(db.String(255), nullable=False) # bisa hyperlink atau internal path ke file
    tumor_id = db.Column(db.Integer, db.ForeignKey('tumor.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Riwayat id=%r nama_lengkap_pasien=%r hasil=%r tanggal=%r waktu=%r gambar=%r tumor_id=%r user_id=%r>' % self.id, self.nama_lengkap_pasien, self.hasil, self.tanggal, self.waktu, self.gambar, self.tumor_id, self.user_id