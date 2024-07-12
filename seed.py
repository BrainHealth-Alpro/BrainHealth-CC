from app import app, db
from app.models import User, Tumor, Riwayat

def seed_data():
    # Create dummy users
    users = [
        {'nama_lengkap': 'Adi Jaya', 'email': 'adi@mail.com', 'nomor_telepon': '082123123123', 'kata_sandi': 'adipassword', 'tipe': 'pasien'},
        {'nama_lengkap': 'Budi Luhur', 'email': 'budi@mail.com', 'nomor_telepon': '082456456456', 'kata_sandi': 'budipassword', 'tipe': 'pasien'},
        {'nama_lengkap': 'Candra Wijaya', 'email': 'candra@mail.com', 'nomor_telepon': '082789789789', 'kata_sandi': 'candrapassword', 'tipe': 'dokter'},
    ]
    
    tumors = [
        {'nama': 'notumor', 'perawatan': 'Anda sehat. Peliharalah gaya hidup yang baik agar terhindar dari penyakit.'},
        {'nama': 'glioma', 'perawatan': '1. Operasi, 2. Terapi Bertarget, 3. Radioterapi, 4. Kemoterapi'},
        {'nama': 'meningioma', 'perawatan': '1. Operasi, 2. Embolisasi Endovaskular, 3. Radioterapi, 4. Kemoterapi'},
        {'nama': 'pituitary', 'perawatan': '1. Pemantauan, 2. Obat-obatan, 3. Operasi, 4. Radioterapi, 5. Terapi radiosensitisasi, 6. Perawatan hormon pengganti'},
    ]
    
    history = [
        {'nama_lengkap_pasien': 'Budi Luhur', 'hasil': 'Terdapat tumor terdeteksi', 'datetime': '2024-07-07 09:10:11','gambar': 'https://commons.wikimedia.org/wiki/File:Glioma.gif#/media/File:Glioma.gif', 'tumor_id': 2, 'user_id': 3} # dokter Candra menangani pasien Budi
    ]

    # Insert users into the database
    for user in users:
        u = User(nama_lengkap=user['nama_lengkap'], email=user['email'], nomor_telepon=user['nomor_telepon'], kata_sandi=user['kata_sandi'], tipe=user['tipe'])
        db.session.add(u)

    for tumor in tumors:
        t = Tumor(nama=tumor['nama'], perawatan=tumor['perawatan'])
        db.session.add(t)

    for history_entry in history:
        h = Riwayat(nama_lengkap_pasien=history_entry['nama_lengkap_pasien'], hasil=history_entry['hasil'], datetime=history_entry['datetime'], gambar=history_entry['gambar'], tumor_id=history_entry['tumor_id'], user_id=history_entry['user_id'])
        db.session.add(h)

    db.session.commit()