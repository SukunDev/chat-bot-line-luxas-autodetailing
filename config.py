import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.urandom(32)

database_username = os.environ.get('FLASK_DATABASE_USERNAME') or ''
database_password = os.environ.get('FLASK_DATABASE_PASSWORD') or ''
database_name = os.environ.get('FLASK_DATABASE_NAME') or ''
database_host = os.environ.get('FLASK_DATABASE_HOST') or ''
database_port = os.environ.get('FLASK_DATABASE_PORT') or ''

# Connect to the database
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}'

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False