from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, jsonify
from apis import api
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

import secrets
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)


from app import app, db
from models import User

@app.route('/')
def index():
    return render_template('index.html')

class RegistrationForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nomor_telepon = PasswordField('Nomor Telepon', validators=[DataRequired()])
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
            return jsonify({'message': 'Login successful', 'email': form.email.data}), 200
        else:
            return jsonify({'message': 'Email or password is incorrect.'}), 400
    else:
        errors = []
        for field, errors_list in form.errors.items():
            for error in errors_list:
                errors.append(f'{field}: {error}')
        return jsonify({'message': 'Validation failed', 'errors': errors}), 400


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

app.run(debug=True, port=80)