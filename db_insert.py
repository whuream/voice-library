# encoding: utf-8
__author__ = 'SuTong'

from voice_library import db, User, Audio, Book

def db_insert():
    kami = User.query.first()

    book1 = Book(u'吃药手册', kami._id)
    book2 = Book(u'治病指南', kami._id)

    audio1 = Audio('', kami._id, 1)
    audio2 = Audio('', kami._id, 2)

    for k in [book1, book2, audio1, audio2]:
        db.session.add(k)

    db.session.commit()

if __name__ == '__main__':
    db_insert()
