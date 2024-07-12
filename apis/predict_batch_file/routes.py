import os
from flask import current_app, jsonify
from flask_restx import Namespace, Resource, abort
from apis.predict_batch_file import model
from werkzeug.datastructures import FileStorage
from datetime import datetime

ns = Namespace('api', description='predict multiple mri images from a zip file')

parser = ns.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True, help='file cannot be empty')
parser.add_argument('nama_pasien', type=str, required=True, help='nama_pasien cannot be empty')
parser.add_argument('user_id', type=int, required=True, help='user_id cannot be empty')

@ns.route('/predict/batchFile')
class PredictBatch(Resource):
    @ns.doc('predict_batch_file')
    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        file = args['file']
        nama_pasien = args['nama_pasien']
        user_id = args['user_id']

        if file.filename == '':
            abort(400, 'No selected file')
        if not file.filename.endswith('.zip') and not file.filename.endswith('.rar'):
            abort(400, 'Only .zip and .rar files are supported')
        try:
            result = model.batch_processing(file, user_id, nama_pasien)
            return jsonify({"result": result})
        except Exception as e:
            print(repr(e))
            current_app.logger.error(e)
            abort(500, 'Internal Server Error')
