import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 # 1 GB
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/brainhealth'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5000

class ProductionConfig(Config):
    DEBUG = False
    PORT = 80