from datetime import datetime
from flask_login import UserMixin

from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(id)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, nullable=False, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        onupdate=datetime.utcnow,
    )
    name = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    reg = db.Column(db.Boolean)
    ed = db.Column(db.Boolean)
    gender= db.Column(db.Boolean)
    coastal = db.Column(db.Boolean)
    loc = db.Column(db.String)    
    group = db.Column(db.Integer)
    block = db.Column(db.Integer)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    hashedid = db.Column(db.String)
    age = db.Column(db.Integer)
    facebookname = db.Column(db.String)
    utm_source = db.Column(db.String)

class Disqualified(UserMixin, db.Model):
    __tablename__ = "disqualified"
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)

class SurveyURL(UserMixin, db.Model):
    __tablename__ = "surveyurl"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        onupdate=datetime.utcnow,
    )
    lang = db.Column(db.String)
    treatmentno = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    updatedby = db.Column(db.String)
