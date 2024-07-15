from flask import jsonify, request, current_app
from flask_restx import Namespace, Resource, abort
from apis.profile import profile
from models import User, db
from werkzeug.datastructures import FileStorage

ns = Namespace('api', description='Manage profile')

parser = ns.parser()
parser.add_argument('id', location='form', type=int, required=True, help='id')
parser.add_argument('nama_lengkap', location='form', type=str, required=False, help='nama_lengkap')
parser.add_argument('email', location='form', type=str, required=False, help='email')
parser.add_argument('nomor_telepon', location='form', type=str, required=False, help='nomor_telepon')
parser.add_argument('gambar', location='files', type=FileStorage, required=False, help='gambar')
parser.add_argument('tempat_lahir', location='form', type=str, required=False, help='tempat_lahir')
parser.add_argument('tanggal_lahir', location='form', type=str, required=False, help='tanggal_lahir')
parser.add_argument('kata_sandi', location='form', type=str, required=False, help='kata_sandi')
parser.add_argument('tipe', location='form', type=str, required=False, help='tipe')

@ns.route('/profile')
class ProfileRoute(Resource):
    @ns.doc('post_profile')
    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        id = args['id']
        nama_lengkap = args['nama_lengkap']
        email = args['email']
        nomor_telepon = args['nomor_telepon']
        gambar = args['gambar']
        tempat_lahir = args['tempat_lahir']
        tanggal_lahir = args['tanggal_lahir']
        kata_sandi = args['kata_sandi']
        tipe = args['tipe']

        return profile.post_profile(id=id, nama_lengkap=nama_lengkap, email=email, nomor_telepon=nomor_telepon, gambar=gambar, tempat_lahir=tempat_lahir, tanggal_lahir=tanggal_lahir, kata_sandi=kata_sandi, tipe=tipe, upload_dir=current_app.config['UPLOAD_FOLDER'])


    @ns.doc('get_profile')
    def get(self):
        user_id = request.args.get('user_id', '')
        user = db.session.query(User).get(user_id)

        if not user:
            return abort(404, 'User not found.')

        return profile.get_profile(user)