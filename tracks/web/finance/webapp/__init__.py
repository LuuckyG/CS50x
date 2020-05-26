from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from webapp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
admin = Admin(template_mode='bootstrap3')

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_obj=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    admin.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from webapp.main.routes import main
    app.register_blueprint(main)

    from webapp.users.routes import users
    app.register_blueprint(users)

    from webapp.transactions.routes import transactions
    app.register_blueprint(transactions)

    from webapp.errors.handlers import errors
    app.register_blueprint(errors)
    
    return app
