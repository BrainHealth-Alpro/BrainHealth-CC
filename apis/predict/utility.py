from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import current_app
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

    def process_file(self, file_name, upload_dir, upload_name=''):
        os.makedirs(upload_dir, exist_ok=True)

        # Check if the file is dicom and process
        if self.is_dicom_by_magic_number(file_name):
            if not file_name.endswith('.dcm'):
                new_file_name = file_name + '.dcm'
                os.rename(file_name, new_file_name)
                file_name = new_file_name
            ndarray = dicom2jpg.dicom2img(file_name)
            file = Image.fromarray(ndarray)
            file_ext = '.jpg'
        else:
            file_ext = os.path.splitext(file_name)[1]
            with open(file_name, 'r') as f:
                file = f.read()

        return self._save(file, file_ext, upload_dir)

    def load_and_preprocess_image(self, image_path, image_shape=(168, 168)):
        img = image.load_img(image_path, target_size=image_shape, color_mode='grayscale')
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def getPrediction(self, file):
        file_temp = self._temp_file(file)
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'img')
        filepath = self.process_file(file_temp, upload_dir)
        img_array = self.load_and_preprocess_image(filepath)
        prediction = self.model.predict(img_array)
        predicted_label = self.class_mappings[np.argmax(prediction)]
        return predicted_label

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
    
    def _save(self, file, ext, upload_dir, upload_name=''):
        if upload_name == '':
            filepath = os.path.join(upload_dir, datetime.now().strftime('%Y%m%d%H%M%S') + ext)
        else:
            filepath = os.path.join(upload_dir, upload_name + ext)
        
        file.save(filepath)
        return filepath
    