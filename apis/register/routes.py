from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.register import register

ns = Namespace('api', description='Register user account')

@ns.route('/register')
class RegisterRoute(Resource):
    @ns.doc('register')
    def post(self):
        args = request.get_json()
        if not args:
            abort(400, 'Invalid JSON')

        required_fields = ['nama_lengkap', 'email', 'nomor_telepon', 'kata_sandi', 'tipe']
        for field in required_fields:
            if field not in args:
                abort(400, f'Missing required field: {field}')

        register.make_form(args)
        return register.validate_register()
