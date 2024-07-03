from flask import jsonify, render_template
from flask_restx import Namespace, Resource, abort
from apis.predict import model
from werkzeug.datastructures import FileStorage

ns = Namespace('predict', description='predict mri images')

mri_image_parser = ns.parser()
mri_image_parser.add_argument('file', location='files', type=FileStorage, required=True, help='file cannot be empty')

@ns.route('/')
class Predict(Resource):
    @ns.doc('predict')
    @ns.expect(mri_image_parser)
    def post(self):
        args = mri_image_parser.parse_args()
        file = args['file']
        if file.filename == '':
            abort(400, 'No selected file')
        result = model.getPrediction(file)
        return jsonify({"result": result})