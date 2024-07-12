from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.login import login

ns = Namespace('api', description='Login CSRF')

@ns.route('/login')
class LoginRoute(Resource):
    @ns.doc('login')
    def post(self):
        args = request.get_json()
        if not args:
            abort(400, 'Invalid JSON')

        required_fields = ['email', 'kata_sandi']
        for field in required_fields:
            if field not in args:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        login.make_form(args)
        return login.validate_login()
