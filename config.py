from os import environ, path
from dotenv import load_dotenv #��������� ���� ����-�������� �� ����� .env 

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'environment/.env'))

DATABASE_HOST = environ.get('DATABASE_HOST')
DATABASE_USERNAME = environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
DATABASE_NAME = environ.get('DATABASE_NAME')
DATABASE_PORT = environ.get('DATABASE_PORT')

SQL_QUERIES_FOLDER = 'sql'
