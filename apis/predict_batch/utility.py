from zipfile import ZipFile

from apis.predict.utility import Predict
import dicom2jpg


class PredictBatch(Predict):
    def __init__(self):
        super().__init__()
        self.results = []
        self.verdict = ''

    def batch_processing(self, file):
        with ZipFile(file.stream, 'r') as zip:
            for zip_info in zip.namelist():
                if zip_info.isdir():
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
