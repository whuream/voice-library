# encoding: utf-8
__author__ = 'SuTong'

from voice_library import db
import datetime


class Audio(db.Model):
    __tablename__ = 'audio'

    _id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String)
    description = db.Column(db.String)
    chapter_number = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book._id'))

    user = db.relationship('User', primaryjoin='Audio.user_id == User._id', backref='audios')
    book = db.relationship('Book', primaryjoin='Audio.book_id == Book._id', backref='audios')

    def __init__(self, file_url, user_id, book_id, chapter_number=1, description=''):
        self.file_url = file_url
        self.description = description
        self.chapter_number = chapter_number
        self.user_id = user_id
        self.book_id = book_id
