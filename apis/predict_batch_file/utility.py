from apis.predict.utility import Predict
from flask import current_app
from PIL import Image
from datetime import datetime
from zipfile import ZipFile
import tempfile
import dicom2jpg
import os
import numpy as np


class PredictBatchFile(Predict):
    def __init__(self):
        super().__init__()
        self.results = []
        self.verdict = ''

    def process_zip(self, file):
        # Make a temporary dir to upload the zip file
        temp_dir = tempfile.mkdtemp()
        
        filepath = os.path.join(temp_dir, 'bismillah_brainhealth_otw_pimnas.zip')
        file.save(filepath)

        return filepath

    def batch_processing(self, file):
        zip_path = self.process_zip(file)

        unzip_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'zip', datetime.now().strftime('%Y%m%d%H%M%S'))

        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        
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
            os.remove(file_path + '.dcm')
            img_array = self.load_and_preprocess_image(jpg_path)
            prediction = self.model.predict(img_array)
            predicted_label = self.class_mappings[np.argmax(prediction)]
            self.results.append({'filename': _file, 'prediction': predicted_label})

        # return self._prediction_handler()
        return self.verdict
    
    # Handle the prediction logic here
    def _prediction_handler(self):
        dict_counter = {
            'Glioma': 0,
            'Meningioma': 0,
            'Notumor': 0,
            'Pituitary': 0,
        }

        for result in self.results:
            dict_counter[result['prediction']] += 1

        self.verdict = max(dict_counter, key=dict_counter.get)
        return dict_counter
