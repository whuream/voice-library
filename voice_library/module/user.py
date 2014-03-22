#encoding: utf-8
__author__ = 'SuTong'

from voice_library import db
import datetime

class User(db.Model):
    __tablename__ = 'user'

    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    date = db.Column(db.DateTime)

    type = db.Column(db.String)

    def __init__(self, uid, password, username='',
                 user_type='', email='', date=datetime.datetime.today()):
        self.id = uid
        self.password = password
        self.email = email
        self.date = date
        self.type = user_type
        self.username = username

