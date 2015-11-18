from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('InPlace.config.DevelConfig')
if 'INPLACE_SETTINGS' in os.environ:
    app.config.from_envvar('INPLACE_SETTINGS')
    
db = SQLAlchemy(app)

import InPlace.controllers
