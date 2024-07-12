from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from models import User, Gambar, db
import os

ns = Namespace('api', description='Upload gambar')

gambar_parser = ns.parser()
gambar_parser.add_argument('path', type=str, location='form', required=True, help='path cannot be empty')

@ns.route('/gambar')
class GambarRoute(Resource):
    @ns.doc('post_gambar')
    @ns.expect(gambar_parser)
    def post(self):
        args = gambar_parser.parse_args()

        path = args['path']
        if path == '':
            abort(400, 'Missing file path')

        new_gambar = Gambar(path=path)
        db.session.add(new_gambar)
        db.session.commit()
        
        # setelah di add ke table, new_gambar bakal punya field baru yaitu id (ini otomatis)
        return jsonify({
            'gambar_id': new_gambar.id,
            'message': 'Image upload successful.'
        })