from flask import jsonify, request
from flask_restx import Namespace, Resource, abort
from apis.history import history
from models import User, db

ns = Namespace('api', description='Manage history')

@ns.route('/history')
class HistoryRoute(Resource):
    @ns.doc('get_history')
    def get(self):
        args = request.get_json()
        user_id = args['user_id']
        user = db.session.query(User).get(user_id)

        if not user:
            return abort(404, 'User not found.')

        return history.get_history(user)