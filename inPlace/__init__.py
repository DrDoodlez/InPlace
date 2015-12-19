from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('InPlace.config.DevelConfig')
if 'INPLACE_SETTINGS' in os.environ:
    app.config.from_envvar('INPLACE_SETTINGS')
    
db = SQLAlchemy(app)

if not app.debug:
    import logging
    file_handler = logging.FileHandler(app.config["LOG_FILE"])
    file_handler.setLevel(logging.DEBUG)

    loggers = [app.logger, logging.getLogger('sqlalchemy')]
    for logger in loggers:
        logger.addHandler(file_handler)
    
import InPlace.controllers
