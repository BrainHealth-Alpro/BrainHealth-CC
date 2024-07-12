from apis.predict_batch_file.utility import PredictBatchFile
from flask import current_app
from datetime import datetime
import requests
import tempfile
import gdown
import os


class PredictBatchLink(PredictBatchFile):
    def __init__(self):
        super().__init__()

    def batch_processing(self, link, user_id, nama_pasien):
        zip_path = self.process_zip(link)
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

    def process_zip(self, file_id):
        url = self.get_download_url(file_id)
        temp_dir = tempfile.mkdtemp()
        destination = os.path.join(temp_dir, 'bismillah_brainhealth_otw_pimnas.zip')
        gdown.download(url, destination, quiet=False)
        return destination

    def is_gdown_link_valid(self, file_id):
        url = self.get_download_url(file_id)
        response = requests.get(url, allow_redirects=True)

        if response.status_code == 200 and 'text/html' not in response.headers['Content-Type']:
            return True
        return False

    def extract_file_id(self, google_drive_url):
        try:
            file_id = google_drive_url.split('/d/')[1].split('/')[0]
            return file_id
        except IndexError:
            return None

    def get_download_url(self, file_id):
        url = f'https://drive.google.com/uc?id={file_id}'
        return url
