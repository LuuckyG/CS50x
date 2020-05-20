from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from webapp.config import Config

admin = Admin(template_mode='bootstrap3')
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app(config_obj=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    admin.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from webapp.routes import main

    app.register_blueprint(main)
    
    return app
