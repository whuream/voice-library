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
        print jsonify(**d).get_data()
        ret[str(book._id)] = jsonify(**d).get_data()

    return jsonify(**ret)


