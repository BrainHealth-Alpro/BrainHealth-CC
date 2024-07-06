from zipfile import ZipFile

from apis.predict.utility import Predict
import dicom2jpg
import os


class PredictBatchFile(Predict):
    def __init__(self):
        super().__init__()
        self.results = []
        self.verdict = ''

    # def process_file(self, file):
        # upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'img')
        # os.makedirs(upload_dir, exist_ok=True)
        #
        # # Check if the file is dicom and process
        # if self._is_dicom_by_magic_number(file):
        #     ndarray = dicom2jpg.dicom2jpg(file)
        #     image = Image.fromarray(ndarray)
        #     file_ext = 'jpg'
        # else:
        #     file_ext = os.path.splitext(file.filename)[1]
        #
        # filepath = os.path.join(upload_dir, datetime.now().strftime('%Y%m%d%H%M%S') + file_ext)
        # file.save(filepath)
        # return filepath

    def batch_processing(self, filepath):
        with ZipFile(filepath, 'r') as zip:
            for zip_info in zip.namelist():
                if zip_info.endswith('/'):
                    continue
                with zip.open(zip_info) as img_file:
                    if zip_info.endswith('.dcm'):
                        img_file = dicom2jpg.dicom2jpg(img_file)
                    result = self.getPrediction(img_file)
                    self.results.append({'filename': zip_info, 'prediction': result})
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
