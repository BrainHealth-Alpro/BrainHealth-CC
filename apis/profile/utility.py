from datetime import datetime
from flask import jsonify, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from models import User, Gambar, db
import os

class ProfileForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()])
    gambar_id = IntegerField('Gambar ID', validators=[DataRequired()])
    tempat_lahir = StringField('Tempat Lahir', validators=[DataRequired()])
    tanggal_lahir = StringField('Tanggal Lahir', validators=[DataRequired()])
    kata_sandi = PasswordField('Kata Sandi', validators=[DataRequired(), EqualTo('kata_sandi')])
    tipe = StringField('Tipe', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class Profile:
    def __init__(self):
        self.form = None

    def post_profile(self):
        if self.form.validate():
            user = User.query.get(self.form.id.data)
            if not user:
                return jsonify({'message': 'User not found.'}), 404

            user.nama_lengkap = self.form.nama_lengkap.data
            user.email = self.form.email.data
            user.nomor_telepon = self.form.nomor_telepon.data
            user.gambar_id = self.form.gambar_id.data
            user.tempat_lahir = self.form.tempat_lahir.data
            user.tanggal_lahir = self.form.tanggal_lahir.data
            user.kata_sandi = self.form.kata_sandi.data
            user.tipe = self.form.tipe.data

            db.session.commit()

            return jsonify({'message': 'Profile updated successfully.'}), 200
        else:
            errors = []
            for field, errors_list in self.form.errors.items():
                for error in errors_list:
                    errors.append(f'{field}: {error}')
            # Gabisa nge return errornya, bingung kyk gimana
            abort (400, 'Validation failed')
            # return jsonify({'message': 'Validation failed', 'errors': errors}), 400

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