# encoding: utf-8
__author__ = 'SuTong'

from voice_library import db, User

def create_db():
    db.create_all()
    kami = User('-', '-', 'kami', 'admin')
    db.session.add(kami)
    db.session.commit()

if __name__ == '__main__':
    create_db()
