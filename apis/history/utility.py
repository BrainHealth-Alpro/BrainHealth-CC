from datetime import datetime
from flask import jsonify, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo
from models import User, Riwayat, Tumor, db
import os

class HistoryForm(FlaskForm):
    nama_lengkap_pasien = StringField('Nama Lengkap Pasien', validators=[DataRequired()])
    hasil = StringField('Hasil', validators=[DataRequired()])
    datetime = DateTimeField('Datetime', validators=[DataRequired()])
    gambar = StringField('Gambar', validators=[DataRequired()])
    tumor_id = IntegerField('Tumor ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Catat History')

class History:
    def __init__(self):
        self.form = None

    def post_history(self):
        if self.form.validate():
            nama_lengkap_pasien = self.form.nama_lengkap_pasien.data
            hasil = self.form.hasil.data
            datetime = self.form.datetime.data
            gambar = self.form.gambar.data
            tumor_id = self.form.tumor_id.data
            user_id = self.form.user_id.data

            # Create a new history
            new_history = Riwayat(nama_lengkap_pasien=nama_lengkap_pasien, hasil=hasil, datetime=datetime,
                                  gambar=gambar, tumor_id=tumor_id, user_id=user_id)
            db.session.add(new_history)
            db.session.commit()

            return jsonify({'message': 'History added successfully.'})
        else:
            errors = []
            for field, errors_list in self.form.errors.items():
                for error in errors_list:
                    errors.append(f'{field}: {error}')
            return jsonify({'message': 'Validation failed', 'errors': errors})

    def get_history(self, user):
        history = db.session.query(Riwayat, Tumor).join(Tumor).filter(Riwayat.tumor_id == Tumor.id).all()

        history_list = [{'id': riwayat.id, 'nama_lengkap_pasien': riwayat.nama_lengkap_pasien,
                        'hasil': riwayat.hasil, 'datetime': riwayat.datetime,
                        'gambar': riwayat.gambar, 'jenis_tumor': tumor.nama, 'user_id': riwayat.user_id } for riwayat, tumor in history]

        return jsonify({'history': history_list})

    def make_form(self, data):
        self.form = HistoryForm(data=data)