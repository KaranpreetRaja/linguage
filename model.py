from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    column1 = db.Column(db.String(1000))
    column2 = db.Column(db.String(1000))
    column3 = db.Column(db.String(1000))
    column4 = db.Column(db.String(1000))
    column5 = db.Column(db.String(1000))
    column6 = db.Column(db.String(1000))
    column7 = db.Column(db.String(1000))
    column8 = db.Column(db.String(1000))