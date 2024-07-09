import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 # 1 GB

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5000

class ProductionConfig(Config):
    DEBUG = False
    PORT = 80