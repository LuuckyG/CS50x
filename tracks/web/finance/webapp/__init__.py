from flask import Flask
from flask_admin import Admin
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from webapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)

admin = Admin(app, template_mode='bootstrap3')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from webapp import routes