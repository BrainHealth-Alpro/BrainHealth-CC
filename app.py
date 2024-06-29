from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request
from apis import api
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        files = {'file': (file.filename, file.stream, file.mimetype)}
        url = 'http://localhost/api/predict'
        response = requests.post(url, files=files)
        filepath = "static/" + file.filename
        predicted_label = response.json()['result']
        return render_template('result.html', prediction=predicted_label, image_path=filepath)

@app.route('/test')
def test():
    # Assuming 'file.jpg' is in the same directory as app.py
    test_image_path = 'static/G_28_RO_.jpg'
    if os.path.exists(test_image_path):
        with open(test_image_path, 'rb') as image_file:
            files = {'file': (test_image_path.split('/')[-1], image_file, 'image/jpeg')}
            url = 'http://localhost/api/predict'
            response = requests.post(url, files=files)
            predicted_label = response.json()['result']
        return render_template('result.html', prediction=predicted_label, image_path=test_image_path)
    else:
        return 'Test image not found'

api.init_app(app)

app.run(debug=True, port=80)