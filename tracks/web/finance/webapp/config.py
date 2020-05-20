import os
from tempfile import mkdtemp


class Config:
    """ Flask application config """

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    TEMPLATES_AUTO_RELOAD = True

    # Admin settings
    FLASK_ADMIN_SWATCH = 'cerulean'

    # Session settings
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
