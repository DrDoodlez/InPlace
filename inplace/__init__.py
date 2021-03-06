from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config.from_object('inplace.config.DevelConfig')
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
    
import inplace.controllers
