import os
basedir = os.path.abspath('%s/../' % os.path.dirname(__file__))

class DefaultConfig:
    DEBUG = False
    LISTEN_HOST = '0.0.0.0'
    LISTEN_PORT = 5000
    WTF_CSRF_ENABLED = True
    SECRET_KEY = '?ZW]eJW2Wf"|P&1P7rPOOXKEv6PHw|ZPjftEY$H^&Vu6q<Z,":<)H@M'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'InPlace.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join(basedir, "boxes/static/uploads/")
    AVATARS_FOLDER = os.path.join(UPLOAD_FOLDER, "avatars/")

    
class DevelConfig(DefaultConfig):
    DEBUG = True

class TestingConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
