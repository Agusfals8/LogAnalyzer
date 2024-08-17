from flask import Flask
from os import environ, path
from dotenv import load_dotenv
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG'] = environ.get('DEBUG') == 'True'

app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(environ.get('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS').lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = environ.get('MAIL_USE_SSL').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')

app.config['UPLOADED_PHOTOS_DEST'] = path.join(basedir, 'uploads')

# Example logging statements
logger.info('Application startup')
logger.warning('This is a warning message')
logger.error('This is an error message')

# Place more logging as needed throughout your application