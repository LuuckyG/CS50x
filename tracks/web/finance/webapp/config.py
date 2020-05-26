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

    # Quote API settings
    API_KEY = os.environ.get('API_KEY')

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    ADMINS = os.environ.get('ADMINS')
