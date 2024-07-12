from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import current_app
from models import Riwayat, Gambar, db
from datetime import datetime
from PIL import Image
import dicom2jpg
import tempfile
import numpy as np
import os

class Predict:
    def __init__(self):
        self.model = load_model('model.h5')
        self.class_mappings = {0: 'Glioma', 1: 'Meningioma', 2: 'Notumor', 3: 'Pituitary'}
        self.filepath = ''

    def get_prediction_from_file(self, file, user_id, nama_pasien):
        file_temp = self._temp_file(file)
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'img')
        prediction = self.predict_util(file_temp, upload_dir)
        self.save_to_db(user_id, nama_pasien, prediction)

        predicted_label = self.class_mappings[prediction]
        return predicted_label
    def predict_util(self, file, upload_dir):
        self.filepath = self.process_file(file, upload_dir)
        img_array = self.load_and_preprocess_image(self.filepath)
        prediction = self.model.predict(img_array)
        return int(np.argmax(prediction))

    def process_file(self, file_name, upload_dir, upload_name=''):
        os.makedirs(upload_dir, exist_ok=True)

        # Check if the file is dicom and process
        if self.is_dicom_by_magic_number(file_name):
            return self.process_dicom(file_name, upload_dir, upload_name)
        else:
            file_ext = os.path.splitext(file_name)[1]
            with open(file_name, 'rb') as f:
                file = f.read()
            return self._save_binary(file, file_ext, upload_dir, upload_name)
        
    def process_dicom(self, file_name, upload_dir, upload_name):
        if not file_name.endswith('.dcm'):
            new_file_name = file_name + '.dcm'
            os.rename(file_name, new_file_name)
            file_name = new_file_name
        ndarray = dicom2jpg.dicom2img(file_name)
        file = Image.fromarray(ndarray)
        file_ext = '.jpg'
        return self._save_image(file, file_ext, upload_dir, upload_name)
    
    def load_and_preprocess_image(self, image_path, image_shape=(168, 168)):
        img = image.load_img(image_path, target_size=image_shape, color_mode='grayscale')
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def is_dicom_by_magic_number(self, file):
        try:
            with open(file, 'rb') as f:
                header = f.read(132)
                return header[128:132] == b'DICM'
        except IOError:
            return False

    def _temp_file(self, file):
        temp_dir = tempfile.mkdtemp()
        temp_name = os.path.join(temp_dir, file.filename)
        file.save(temp_name)
        return temp_name

    def _save_image(self, file, ext, upload_dir, upload_name=''):
        if upload_name == '':
            filepath = os.path.join(upload_dir, datetime.now().strftime('%Y%m%d%H%M%S') + ext)
        else:
            filepath = os.path.join(upload_dir, upload_name + ext)
        
        file.save(filepath)
        return filepath

    def _save_binary(self, file_content, ext, upload_dir, upload_name=''):
        if upload_name == '':
            filename = datetime.now().strftime('%Y%m%d%H%M%S') + ext
        else:
            filename = upload_name + ext
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(file_content)
        return filepath

    def save_to_db(self, user_id, nama_pasien, prediction):
        gambar_id = self._save_gambar_to_db()
        self._save_history_to_db(user_id, nama_pasien, prediction, gambar_id)

    def _save_gambar_to_db(self):
        new_gambar = Gambar(path=self.filepath)
        db.session.add(new_gambar)
        db.session.commit()
        return new_gambar.id

    def _save_history_to_db(self, user_id, nama_pasien, prediction, gambar_id):
        nama_lengkap_pasien = nama_pasien
        if prediction == 0:
            hasil = 'Tidak ada tumor terdeteksi'
        else:
            hasil = 'Terdapat tumor yang terdeteksi'

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        tumor_id = prediction + 1
        user_id = user_id

        new_history = Riwayat(nama_lengkap_pasien=nama_lengkap_pasien, hasil=hasil, datetime=date,
                              gambar_id=gambar_id, tumor_id=tumor_id, user_id=user_id)

        db.session.add(new_history)
        db.session.commit()