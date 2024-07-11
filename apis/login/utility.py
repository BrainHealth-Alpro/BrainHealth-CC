from flask import jsonify, abort
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    kata_sandi = PasswordField('Kata Sandi', validators=[DataRequired(), EqualTo('kata_sandi')])
    submit = SubmitField('Masuk')

class Login():
    def __init__(self):
        self.form = None

    def validate_login(self):
        if self.form.validate():
            user = User.query.filter_by(email=self.form.email.data).first()
            if user and user.check_password(self.form.kata_sandi.data):
                return jsonify({'message': 'Login successful', 'id': user.id, 'email': self.form.email.data})
            else:
                abort(400, 'Email or password is incorrect')
        else:
            errors = []
            for field, error_list in self.form.errors.items():
                for error in error_list:
                    errors.append(f'{field}: {error}')
            return abort(400, {'message': 'Login failed', 'errors': errors})

    def make_form(self, data):
        self.form = LoginForm(data=data)
