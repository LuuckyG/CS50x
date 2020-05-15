from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from webapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from webapp import routes