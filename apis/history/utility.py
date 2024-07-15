from flask import jsonify, abort
from models import User, Riwayat, Tumor, Gambar, db

class History:
    def __init__(self):
        self.form = None

    def get_history(self, user_id):
        history = db.session.query(Riwayat, Tumor, Gambar) \
            .join(Tumor, Riwayat.tumor_id == Tumor.id) \
            .join(Gambar, Riwayat.gambar_id == Gambar.id) \
            .filter(Riwayat.user_id == user_id) \
            .all()

        history_list = [{'id': riwayat.id, 'nama_lengkap_pasien': riwayat.nama_lengkap_pasien,
                         'hasil': riwayat.hasil, 'datetime': riwayat.datetime,
                         'gambar_path': gambar.path, 'jenis_tumor': tumor.nama, 'user_id': riwayat.user_id}
                        for riwayat, tumor, gambar in history]

        return jsonify({'history': history_list})
