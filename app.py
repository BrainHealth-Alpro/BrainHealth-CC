import logging
from logging.handlers import RotatingFileHandler

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, jsonify
from apis import api
from config import DevelopmentConfig, ProductionConfig
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

import secrets
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)


from app import app, db
from models import User, Riwayat, Tumor

app.config.from_object(DevelopmentConfig)
# # Uncomment below for production
# app.config.from_object(ProductionConfig)

# Set logging
handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=10)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('index.html')

class RegistrationForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()])
    kata_sandi = PasswordField('Kata Sandi', validators=[DataRequired(), EqualTo('kata_sandi')])
    tipe = StringField('Tipe', validators=[DataRequired()])
    submit = SubmitField('Buat Akun')
    
@app.route('/api/csrf', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid JSON'}), 400

    required_fields = ['nama_lengkap', 'email', 'nomor_telepon', 'kata_sandi', 'tipe']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    form = RegistrationForm(data=data)

    if form.validate():
        nama_lengkap = form.nama_lengkap.data
        email = form.email.data
        nomor_telepon = form.nomor_telepon.data
        kata_sandi = form.kata_sandi.data
        tipe = form.tipe.data

        # Check if the name or email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Username or email already exists. Please choose a different one.'}), 400

        # Create a new user
        new_user = User(nama_lengkap=nama_lengkap, email=email, nomor_telepon=nomor_telepon, kata_sandi=kata_sandi, tipe=tipe)
        new_user.set_password(kata_sandi)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful. You can now log in.'}), 201
    else:
        errors = []
        for field, errors_list in form.errors.items():
            for error in errors_list:
                errors.append(f'{field}: {error}')
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    kata_sandi = PasswordField('Kata Sandi', validators=[DataRequired(), EqualTo('kata_sandi')])
    submit = SubmitField('Masuk')
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid JSON'}), 400

    required_fields = ['email', 'kata_sandi']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    form = LoginForm(data=data)

    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.kata_sandi.data):
            return jsonify({'message': 'Login successful', 'id': user.id, 'email': form.email.data}), 200
        else:
            return jsonify({'message': 'Email or password is incorrect.'}), 400
    else:
        errors = []
        for field, errors_list in form.errors.items():
            for error in errors_list:
                errors.append(f'{field}: {error}')
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400


class HistoryForm(FlaskForm):
    nama_lengkap_pasien = StringField('Nama Lengkap Pasien', validators=[DataRequired()])
    hasil = StringField('Hasil', validators=[DataRequired()])
    datetime = DateTimeField('Datetime', validators=[DataRequired()])
    gambar = StringField('Gambar', validators=[DataRequired()])
    tumor_id = IntegerField('Tumor ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Catat History')
    

@app.route('/history', methods=['POST'])
def post_history():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid JSON'}), 400

    required_fields = ['nama_lengkap_pasien', 'hasil', 'datetime', 'gambar', 'tumor_id', 'user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    form = HistoryForm(data=data)

    if form.validate():
        nama_lengkap_pasien = form.nama_lengkap_pasien.data
        hasil = form.hasil.data
        datetime = form.datetime.data
        gambar = form.gambar.data
        tumor_id = form.tumor_id.data
        user_id = form.user_id.data

        # Create a new history
        new_history = Riwayat(nama_lengkap_pasien=nama_lengkap_pasien, hasil=hasil, datetime=datetime, gambar=gambar, tumor_id=tumor_id, user_id=user_id)
        db.session.add(new_history)
        db.session.commit()

        return jsonify({'message': 'History added successfully.'}), 201
    else:
        errors = []
        for field, errors_list in form.errors.items():
            for error in errors_list:
                errors.append(f'{field}: {error}')
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400
    

@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id', '')
    history = db.session.query(Riwayat, Tumor).join(Tumor).filter(Riwayat.tumor_id == Tumor.id).all()
    #history = Riwayat.query.filter_by(user_id=user_id).all()
    
    if not history:
        return jsonify({'history': [], 'message': 'History not found.'}), 400

    history_list = [{'id': riwayat.id, 'nama_lengkap_pasien': riwayat.nama_lengkap_pasien,
                        'hasil': riwayat.hasil, 'datetime': riwayat.datetime,
                        'gambar': riwayat.gambar, 'jenis_tumor': tumor.nama, 'user_id': riwayat.user_id } for riwayat, tumor in history]
    return jsonify({'history': history_list}), 200


class ProfileForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nomor_telepon = StringField('Nomor Telepon', validators=[DataRequired()])
    foto_profil = StringField('Foto Profil', validators=[DataRequired()])
    tempat_lahir = StringField('Tempat Lahir', validators=[DataRequired()])
    tanggal_lahir = StringField('Tanggal Lahir', validators=[DataRequired()])
    kata_sandi = PasswordField('Kata Sandi', validators=[DataRequired(), EqualTo('kata_sandi')])
    tipe = StringField('Tipe', validators=[DataRequired()])
    submit = SubmitField('Update Profile')


@app.route('/profile', methods=['POST'])
def update_profile():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid JSON'}), 400

    required_fields = ['id', 'nama_lengkap', 'email', 'nomor_telepon', 'foto_profil', 'tempat_lahir', 'tanggal_lahir', 'kata_sandi', 'tipe']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    form = ProfileForm(data=data)

    if form.validate():
        user = User.query.get(form.id.data)
        if not user: # seharusnya ngga pernah kejadian gini sih wkwkwk (kecuali ada orang yang pake browser coba2 api kita)
            return jsonify({'message': 'User not found.'}), 404

        user.nama_lengkap = form.nama_lengkap.data
        user.email = form.email.data
        user.nomor_telepon = form.nomor_telepon.data
        user.foto_profil = form.foto_profil.data
        user.tempat_lahir = form.tempat_lahir.data
        user.tanggal_lahir = form.tanggal_lahir.data
        user.kata_sandi = form.kata_sandi.data
        user.tipe = form.tipe.data

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully.'}), 200
    else:
        errors = []
        for field, errors_list in form.errors.items():
            for error in errors_list:
                errors.append(f'{field}: {error}')
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400
    

@app.route('/profile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id', '')
    user = db.session.query(User).get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    return jsonify({
        'id': user.id,
        'nama_lengkap': user.nama_lengkap,
        'email': user.email,
        'nomor_telepon': user.nomor_telepon,
        'foto_profil': user.foto_profil,
        'tempat_lahir': user.tempat_lahir,
        'tanggal_lahir': user.tanggal_lahir,
        'kata_sandi': user.kata_sandi,
        'tipe': user.tipe,
    }), 200


@app.route('/result', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        files = {'file': (file.filename, file.stream, file.mimetype)}
        url = 'http://localhost/api/predict'
        response = requests.post(url, files=files)
        filepath = "static/" + file.filename
        predicted_label = response.json()['result']
        return render_template('result.html', prediction=predicted_label, image_path=filepath)

@app.route('/test')
def test():
    # Assuming 'file.jpg' is in the same directory as app.py
    test_image_path = 'static/G_28_RO_.jpg'
    if os.path.exists(test_image_path):
        with open(test_image_path, 'rb') as image_file:
            files = {'file': (test_image_path.split('/')[-1], image_file, 'image/jpeg')}
            url = 'http://localhost/api/predict'
            response = requests.post(url, files=files)
            predicted_label = response.json()['result']
        return render_template('result.html', prediction=predicted_label, image_path=test_image_path)
    else:
        return 'Test image not found'

api.init_app(app)

app.run()