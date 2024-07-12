from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.gambar import gambar
from werkzeug.datastructures import FileStorage
from models import User, Gambar, db

ns = Namespace('api', description='Upload  gambar')

gambar_parser = ns.parser()
gambar_parser.add_argument('file', location='files', type=FileStorage, required=True, help='file cannot be empty')
gambar_parser.add_argument('type', type=str, location='form', required=True, help='type of image (profile_photo or history_image)')

@ns.route('/gambar')
class GambarRoute(Resource):
    @ns.doc('post_gambar')
    @ns.expect(gambar_parser)
    def post(self):
        args = gambar_parser.parse_args()
        file = args['file']
        if file.filename == '':
            abort(400, 'No selected file')
            
        ftype = args['type']
        if ftype == '':
            abort(400, 'Missing file type')

        filename = file.filename
        file_extension = os.path.splitext(filename)[1]

        # ini path ke file di storage
        path = profile_photo._save_image(file=file, ext=file_extension, ftype=ftype)
        
        new_gambar = Gambar(path=path)
        db.session.add(new_gambar)
        db.session.commit()
        
        # setelah di add ke table, new_gambar bakal punya field baru yaitu id (ini otomatis)
        return jsonify({
            'gambar_id': new_gambar.id,
            'message': 'Image upload successful.'
        }), 201