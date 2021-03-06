import os
basedir = os.path.abspath('%s/../' % os.path.dirname(__file__))

class DefaultConfig:
    DEBUG = True
    LISTEN_HOST = '0.0.0.0'
    LISTEN_PORT = 5000
    WTF_CSRF_ENABLED = True
    SECRET_KEY = '?ZW]eJW2Wf"|P&1P7rPOOXKEv6PHw|ZPjftEY$H^&Vu6q<Z,":<)H@M'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'inplace.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join(basedir, "inplace/static/uploads/")
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPEG'])
    AVATARS_FOLDER = os.path.join(UPLOAD_FOLDER, "avatars/")
    PHOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, "photos/")
    LOG_FILE = os.path.join(basedir, "inplace.log")


    
class DevelConfig(DefaultConfig):
    DEBUG = True

class TestingConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
