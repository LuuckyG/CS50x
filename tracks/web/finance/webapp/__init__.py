from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from webapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)
Session(app)
db = SQLAlchemy(app)

from webapp import routes