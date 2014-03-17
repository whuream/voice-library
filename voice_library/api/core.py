# encoding: utf-8
__author__ = 'SuTong'

from voice_library import *
from flask import request, session, jsonify
from sqlalchemy.sql.expression import and_


@app.route('/api/verify_user', methods=['POST'])
def verify_user():
    uid = request.form['uid']
    password = request.form['password']

    user = User.query.filter(and_(User.id == uid, User.password == password)).first()
    if user:
        session['uid'] = user._id
        #print session.viewitems()
        #print dir(session)
        return '1'
    else:
        return '0'

@app.route('/api/get_book_list', methods=['GET'])
def get_book_list():
    books = Book.query.all()
    t = []
    ret = {}
    for book in books:
        d = {'name': book.name, 'author': book.author, 'cover': book.cover,
             'content': book.content, 'file_url': book.file_url, 'description': book.description,
             'chapter_number': book.chapter_number, 'date': book.date}
        #print jsonify(**d).get_data()
        ret[str(book._id)] = jsonify(**d).get_data()

    return jsonify(**ret)

@app.route('/api/get_book_info', methods=['POST'])
def get_book_info():
    book_id = request.form['bid']
    book = Book.query.filter(Book._id == book_id).first()
    if not book:
        return '0'
    else:
        ret = {}
        print book.audios
        for audio in book.audios:
            d = {'file_url': audio.file_url, 'description': audio.description,
                 'chapter_number': audio.chapter_number, 'user_id': audio.user_id}
            print jsonify(**d).get_data()
            ret[str(audio._id)] = jsonify(**d).get_data()

        return jsonify(**ret)

@app.route('/api/get_user_info', methods=['POST'])
def get_user_info():
    uid = request.form['uid']
    user = User.query.filter(User._id == uid).first()
    if not user:
        return '0'
    else:
        ret = {'uid': user._id, 'id': user.id, 'name': user.username,
               'email': user.email, 'type': user.type}
        return jsonify(**ret)