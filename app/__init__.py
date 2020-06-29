from flask import Flask, request, session
from flask_bootstrap import Bootstrap
from os import path

app = Flask(__name__)
app.config.from_object("config")
bootstrap = Bootstrap(app)

from app import views # noqa: E402,F401
