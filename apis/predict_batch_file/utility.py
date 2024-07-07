from apis.predict.utility import Predict
from flask import current_app
from PIL import Image
from datetime import datetime
from zipfile import ZipFile
import tempfile
import dicom2jpg
import os


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
        file_list = os.listdir(dir_source)
        
        # Dealing with nested folder in the zip file, need to search better methods to do so
        if file_list[0].endswith('/'):
            file_list = os.listdir(
                os.path.join(
                    unzip_path,
                    file_list[0],
                )
            )

            dir_source = os.path.join(dir_source, file_list[0])

        # for _file in file_list:
        #     _file_path = self.process_file()

        # with ZipFile(zip_path, 'r') as zip_ref:
        #     for zip_info in zip_ref.namelist():
        #         if zip_info.endswith('/'):
        #             continue
        #         with zip_ref.open(zip_info) as img_file:
        #             if zip_info.endswith('.dcm'):
        #                 img_file = dicom2jpg.dicom2jpg(img_file)
        #             result = self.getPrediction(img_file)
        #             self.results.append({'filename': zip_info, 'prediction': result})
        self._prediction_handler()
        return self.verdict

    def _prediction_handler(self):
        dict_counter = {
            'Glioma': 0,
            'Meningioma': 0,
            'NoTumor': 0,
            'Pituitary': 0,
        }

        for result in self.results:
            dict_counter[result['prediction']] += 1

        self.verdict = max(dict_counter, key=dict_counter.get)
