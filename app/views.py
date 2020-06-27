from flask import g, render_template, redirect, request, session, url_for, flash
from app import app, db
import requests

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')    

