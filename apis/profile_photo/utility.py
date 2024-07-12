from datetime import datetime
from flask import jsonify, abort, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from models import User, db
import os

class ProfilePhoto:
    def _save_image(self, file, ext, upload_dir=current_app.config['UPLOAD_FOLDER'], upload_name=''):
        if upload_name == '':
            filepath = os.path.join(upload_dir + '/profile_photos', datetime.now().strftime('%Y%m%d%H%M%S') + ext)
        else:
            filepath = os.path.join(upload_dir + '/profile_photos', upload_name + ext)
        
        file.save(filepath)
        return filepath