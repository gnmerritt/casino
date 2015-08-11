from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config.from_object('matchmaker.default_settings')
app.config.from_envvar('CASINO_SETTINGS', silent=True)

db = SQLAlchemy(app)

import models
import login
import views
import api
