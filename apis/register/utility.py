from flask import jsonify, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from models import User, db

class RegisterForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()])
    kata_sandi = PasswordField('Kata Sandi', validators=[DataRequired(), EqualTo('kata_sandi')])
    tipe = StringField('Tipe', validators=[DataRequired()])
    submit = SubmitField('Buat Akun')

class Register():
    def __init__(self):
        self.form = None

    def validate_register(self):
        if self.form.validate():
            nama_lengkap = self.form.nama_lengkap.data
            email = self.form.email.data
            nomor_telepon = self.form.nomor_telepon.data
            kata_sandi = self.form.kata_sandi.data
            tipe = self.form.tipe.data

            # Check if the name or email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return abort(400, {'message': 'Username or email already exists. Please choose a different one.'})

            # Create a new user
            new_user = User(nama_lengkap=nama_lengkap, email=email, nomor_telepon=nomor_telepon, kata_sandi=kata_sandi,
                            tipe=tipe)
            new_user.set_password(kata_sandi)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'Registration successful. You can now log in.'})
        else:
            errors = []
            for field, errors_list in self.form.errors.items():
                for error in errors_list:
                    errors.append(f'{field}: {error}')
            return abort(400, ({'message': 'Validation failed', 'errors': errors}))

    def make_form(self, data):
        self.form = RegisterForm(data=data)
