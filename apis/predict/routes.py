from flask import jsonify, render_template, request
from flask_restx import Namespace, Resource, abort
from apis.predict import model
from werkzeug.datastructures import FileStorage

ns = Namespace('api', description='predict mri images')

parser = ns.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True, help='file cannot be empty')
parser.add_argument('nama_pasien', type=str, required=True, help='nama_pasien cannot be empty')
parser.add_argument('user_id', type=int, required=True, help='user_id cannot be empty')

@ns.route('/predict')
class Predict(Resource):
    @ns.doc('predict')
    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        file = args['file']
        nama_pasien = args['nama_pasien']
        user_id = args['user_id']

        if file.filename == '':
            abort(400, 'No selected file')

        result = model.get_prediction_from_file(user_id, file, nama_pasien)
        return jsonify({"result": result})