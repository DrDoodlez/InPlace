from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('boxes.config.DevelConfig')
if 'BOXES_SETTINGS' in os.environ:
    app.config.from_envvar('BOXES_SETTINGS')
    
db = SQLAlchemy(app)

import boxes.controllers
