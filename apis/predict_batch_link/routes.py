import os
from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.predict_batch_link import model
from werkzeug.datastructures import FileStorage

ns = Namespace('api', description='predict multiple mri images from a zip file with google drive link')


@ns.route('/predict/batchLink')
class PredictBatch(Resource):
    @ns.doc('predict_batch_link')
    def post(self):
        args = request.get_json()
        if not args:
            abort(400, 'Invalid JSON')
        link = args['link']
        user_id = args['user_id']
        nama_pasien = args['nama_pasien']
        file_id = model.extract_file_id(link)

        if model.is_gdown_link_valid(file_id):
            abort(400, 'Link invalid')
        try:
            result = model.batch_processing(file_id, user_id, nama_pasien)
            return jsonify({"result": result})
        except Exception as e:
            print(repr(e))
            current_app.logger.error(e)
            abort(500, 'Internal Server Error')
