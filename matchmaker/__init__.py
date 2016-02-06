import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import slacker_log_handler as slh

app = Flask(__name__, static_folder='static')
app.config.from_object('matchmaker.default_settings')
app.config.from_envvar('CASINO_SETTINGS', silent=True)

if not app.debug or True:
    handler = slh.SlackerLogHandler(
        app.config['SLACK_API_KEY'],
        app.config['SLACK_CHANNEL'],
        username=app.config['SLACK_USERNAME']
    )
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info("Casino Matchmaker webapp restarted")

db = SQLAlchemy(app)

import models
import login
import views
import api
