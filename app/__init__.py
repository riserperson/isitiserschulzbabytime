from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from os import path
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
        return session.get('lang')
    elif 'lang' in session.keys():
        return session['lang']
    else:
        session['lang'] = request.accept_languages.best_match(app.config['LANGUAGES'])
        if session['lang'] is None:
            print request.accept_languages
        return request.accept_languages.best_match(app.config['LANGUAGES'])

from app import views, models  # noqa: E402,F401
