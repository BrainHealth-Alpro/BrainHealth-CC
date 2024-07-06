from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import current_app
from datetime import datetime
from PIL import Image
import dicom2jpg
import numpy as np
import os

class Predict:
    def __init__(self):
        self.model = load_model('model.h5')
        self.class_mappings = {0: 'Glioma', 1: 'Meningioma', 2: 'Notumor', 3: 'Pituitary'}

    def process_file(self, file):
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'img')
        os.makedirs(upload_dir, exist_ok=True)

        # Check if the file is dicom and process
        if self._is_dicom_by_magic_number(file):
            ndarray = dicom2jpg.dicom2jpg(file)
            image = Image.fromarray(ndarray)
            file_ext = 'jpg'
        else:
            file_ext = os.path.splitext(file.filename)[1]

        filepath = os.path.join(upload_dir, datetime.now().strftime('%Y%m%d%H%M%S') + file_ext)
        file.save(filepath)
        return filepath

    def load_and_preprocess_image(self, image_path, image_shape=(168, 168)):
        img = image.load_img(image_path, target_size=image_shape, color_mode='grayscale')
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def getPrediction(self, file):
        filepath = self.process_file(file)
        img_array = self.load_and_preprocess_image(filepath)
        prediction = self.model.predict(img_array)
        predicted_label = self.class_mappings[np.argmax(prediction)]
        return predicted_label

    def _is_dicom_by_magic_number(self, file):
        try:
            header = file.read(132)
            return header[128:132] == b'DICM'
        except IOError:
            return False
        finally:
            file.seek(0)