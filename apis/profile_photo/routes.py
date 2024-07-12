from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.profile_photo import profile_photo
from werkzeug.datastructures import FileStorage
from models import User, Gambar, db

ns = Namespace('api', description='Upload profile photo')

profile_photo_parser = ns.parser()
profile_photo_parser.add_argument('file', location='files', type=FileStorage, required=True, help='file cannot be empty')

@ns.route('/profile_photo')
class ProfilePhotoRoute(Resource):
    @ns.doc('post_profile_photo')
    @ns.expect(profile_photo_parser)
    def post(self):
        args = profile_photo_parser.parse_args()
        file = args['file']
        if file.filename == '':
            abort(400, 'No selected file')

        filename = file.filename
        file_extension = os.path.splitext(filename)[1]

        # ini path ke file di storage
        path = profile_photo._save_image(file, file_extension, 'profile_photos')
        
        new_gambar = Gambar(path=path)
        db.session.add(new_gambar)
        db.session.commit()
        
        # setelah di add ke table, new_gambar bakal punya field baru yaitu id (ini otomatis)
        return jsonify({
            'gambar_id': new_gambar.id,
            'message': 'Photo profile upload successful.'
        }), 201