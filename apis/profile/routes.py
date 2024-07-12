from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.profile import profile
from models import User, db

ns = Namespace('api', description='Manage profile')

@ns.route('/profile')
class ProfileRoute(Resource):
    @ns.doc('post_profile')
    def post(self):
        args = request.get_json()

        if not args:
            abort(400, 'Invalid JSON')

        required_fields = ['id', 'nama_lengkap', 'email', 'nomor_telepon', 'gambar_id', 'tempat_lahir',
                           'tanggal_lahir', 'kata_sandi', 'tipe']
        for field in required_fields:
            if field not in args:
                return abort(400, 'Missing required field')

        profile.make_form(args)
        return profile.post_profile()


    @ns.doc('get_profile')
    def get(self):
        user_id = request.args.get('user_id', '')
        user = db.session.query(User).get(user_id)

        if not user:
            return abort(404, 'User not found.')

        return profile.get_profile(user)