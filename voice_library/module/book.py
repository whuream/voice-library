# encoding: utf-8
__author__ = 'SuTong'

from voice_library import db
import datetime

class Book(db.Model):
    __tablename__ = 'book'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    author = db.Column(db.String)
    cover = db.Column(db.String)
    content = db.Column(db.String)
    file_url = db.Column(db.String)
    description = db.Column(db.String)
    chapter_number = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user._id'))

    user = db.relationship('User', primaryjoin='Book.user_id == User._id', backref='books')

    def __init__(self, name, user_id, chapter_number=1, content='', file_url='', author='',
                 cover='', description='', date=datetime.datetime.today()):
        self.name = name
        self.author = author
        self.cover = cover
        self.description = description
        self.chapter_number=chapter_number
        self.date = date
        self.user_id = user_id
        self.content = content
        self.file_url = file_url