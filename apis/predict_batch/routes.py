from flask import jsonify, render_template
from flask_restx import Namespace, Resource, abort
from apis.predict_batch import model
from werkzeug.datastructures import FileStorage

ns = Namespace('predict_batch', description='predict multiple mri images from a zip file')

zip_parser = ns.parser()
zip_parser.add_argument('file', location='files', type=FileStorage, required=True, help='file cannot be empty')


@ns.route('/')
class PredictBatch(Resource):
    @ns.doc('predict_batch')
    @ns.expect(zip_parser)
    def post(self):
        args = zip_parser.parse_args()
        file = args['file']
        if file.filename == '':
            abort(400, 'No selected file')
        if not file.filename.endswith('.zip'):
            abort(400, 'Only .zip files are supported')
        result = model.batch_processing(file)
        return jsonify({"result": result}), 200
