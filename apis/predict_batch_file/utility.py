from apis.predict.utility import Predict
from flask import current_app
from datetime import datetime
from zipfile import ZipFile
from rarfile import RarFile
import tempfile
import os
import numpy as np


class PredictBatchFile(Predict):
    def __init__(self):
        super().__init__()
        self.results = []
        self.verdict = ''
        self.filepath = os.path.join(os.getcwd(), 'static', 'zip_img.jpg')

    def batch_processing(self, file, user_id, nama_pasien):
        zip_path = self.process_zip(file)
        self.extract_and_assign_diagnosis(zip_path)
        self.count_diagnosis()
        if self.verdict == 'Glioma':
            prediction = 0
        elif self.verdict == 'Meningioma':
            prediction = 1
        elif self.verdict == 'Notumor':
            prediction = 2
        elif self.verdict == 'Pituitary':
            prediction = 3
        self.save_to_db(user_id, nama_pasien, prediction)
        return self.verdict

    def process_zip(self, file):
        # Make a temporary dir to upload the zip file
        temp_dir = tempfile.mkdtemp()
        
        filepath = os.path.join(temp_dir, file.filename)
        file.save(filepath)

        return filepath

    def extract_and_assign_diagnosis(self, zip_path):
        unzip_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'zip', datetime.now().strftime('%Y%m%d%H%M%S'))

        if zip_path.endswith('.zip'):
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
        elif zip_path.endswith('.rar'):
            with RarFile(zip_path, 'r') as rar_file:
                rar_file.extractall(unzip_path)
        
        dir_source = unzip_path

        for root, dirs, files in os.walk(dir_source):
            for file in files:
                continue
            for dir in dirs:
                # Can be modified just in case we want to have multiple dirs
                dir_source = os.path.join(root, dir)
                file_list = os.listdir(dir_source)
                break

        for _file in file_list:
            file_path = os.path.join(dir_source, _file)
            jpg_path = self.process_dicom(file_path, dir_source, _file)
            if '.dcm' in file_path:
                os.remove(file_path)
            else:
                os.remove(file_path + '.dcm')
            img_array = self.load_and_preprocess_image(jpg_path)
            prediction = self.model.predict(img_array)
            predicted_label = self.class_mappings[np.argmax(prediction)]
            self.results.append({'filename': _file, 'prediction': predicted_label})
    
    # Handle the prediction logic here
    def count_diagnosis(self):
        dict_counter = {
            'Glioma': 0,
            'Meningioma': 0,
            'Notumor': 0,
            'Pituitary': 0,
        }

        for result in self.results:
            dict_counter[result['prediction']] += 1

        self.verdict = max(dict_counter, key=dict_counter.get)
