from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from flask_wtf.csrf import generate_csrf

ns = Namespace('api', description='Get CSRF Token')

@ns.route('/csrf')
class CSRFRoute(Resource):
    @ns.doc('csrf')
    def get(self):
        token = generate_csrf()
        response = make_response(jsonify({'csrf_token': token}))
        response.set_cookie('csrf_token', token)
        return response
