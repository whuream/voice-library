__author__ = 'SuTong'


from voice_library import db
import datetime

class Like(db.Model):
    __tablename__ = 'like'

    _id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user._id'))
    user = db.relationship('User', primaryjoin='Like.user_id == User._id', backref='likes')

    book_id = db.Column(db.Integer, db.ForeignKey('book._id'))
    book = db.relationship('Book', primaryjoin='Like.book_id == Book._id', backref='likes')

    date = db.Column(db.DateTime)

    def __init__(self, user_id, book_id, date=datetime.datetime.today()):
        self.user_id = user_id
        self.book_id = book_id
        self.date = date