from datetime import datetime
from flask import jsonify, abort, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from models import User, Gambar, db
import os

class Profile:
    def __init__(self):
        self.form = None
        
    def _save_image(self, file, ext, upload_dir, upload_name=''):
        if upload_name == '':
            filepath = os.path.join(upload_dir + '/profile_photos', datetime.now().strftime('%Y%m%d%H%M%S') + ext)
        else:
            filepath = os.path.join(upload_dir + '/profile_photos', upload_name + ext)
        
        file.save(filepath)
        return filepath
        

    def post_profile(self, id, nama_lengkap, email, nomor_telepon, gambar, filename, tempat_lahir, tanggal_lahir, kata_sandi, tipe, upload_dir):
        user = User.query.get(id)
        if not user:
            return abort(404, "User not found.")

        user.nama_lengkap = nama_lengkap
        user.email = email
        user.nomor_telepon = nomor_telepon
        
        # impement file saving logic
        path = self._save_image(gambar, os.path.splitext(filename)[1], upload_dir=upload_dir)
        
        new_gambar = Gambar(path=path)
        db.session.add(new_gambar)
        db.session.commit()

        user.gambar_id = new_gambar.id
        user.tempat_lahir = tempat_lahir
        user.tanggal_lahir = tanggal_lahir
        user.kata_sandi = kata_sandi
        user.tipe = tipe

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully.'})

    def get_profile(self, user):
        foto_profil_path = db.query(Gambar).get(user.gambar_id)
        return jsonify({
            'id': user.id,
            'nama_lengkap': user.nama_lengkap,
            'email': user.email,
            'nomor_telepon': user.nomor_telepon,
            'foto_profil_path': foto_profil_path,
            'tempat_lahir': user.tempat_lahir,
            'tanggal_lahir': user.tanggal_lahir,
            'kata_sandi': user.kata_sandi,
            'tipe': user.tipe,
        })

    def make_form(self, data):
        self.form = ProfileForm(data=data)