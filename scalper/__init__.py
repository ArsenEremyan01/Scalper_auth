from flask import Flask
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'YOUR SECRET KEY'  # TODO
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:W5w5y599@localhost/scalper_auth_DB'  # TODO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
RECAPTCHA_SITE_KEY = "6LfhyLoeAAAAABVRtvu-qxOCnTkuT04Gq31o7o4b"  # your site key TODO
RECAPTCHA_SECRET_KEY = "6LfhyLoeAAAAAIyXV4fxThW-N65sa2bqhQtOsxBA"  # your secret key TODO
recaptcha = ReCaptcha(app)
db = SQLAlchemy(app)
manager = LoginManager(app)

from scalper import models, routes

db.create_all()
