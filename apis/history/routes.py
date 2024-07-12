from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.history import history
from models import User, db

ns = Namespace('api', description='Manage history')

@ns.route('/history')
class HistoryRoute(Resource):
    @ns.doc('post_history')
    def post(self):
        args = request.get_json()

        if not args:
            abort(400, 'Invalid JSON')

        required_fields = ['nama_lengkap_pasien', 'hasil', 'datetime', 'gambar_id', 'tumor_id', 'user_id']

        for field in required_fields:
            if field not in args:
                return abort(400, 'Missing required field')

        history.make_form(args)
        return history.post_history()


    @ns.doc('get_history')
    def get(self):
        user_id = request.args.get('user_id', '')
        user = db.session.query(User).get(user_id)

        if not user:
            return abort(404, 'User not found.')

        return history.get_history(user)