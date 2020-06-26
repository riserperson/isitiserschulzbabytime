import os
from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = False
SECRET_KEY = "ozymandias"
LANGUAGES = ['en', 'fr', 'ar', 'en_US', 'ar_TN', 'fr_FR']

# Database details
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIRECTORY, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
