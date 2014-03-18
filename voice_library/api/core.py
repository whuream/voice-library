# encoding: utf-8
__author__ = 'SuTong'

from voice_library import *
from flask import request, session, jsonify
from sqlalchemy.sql.expression import and_
import os
from datetime import datetime
from werkzeug.utils import secure_filename


@app.route('/api/verify_user', methods=['POST'])
def verify_user():
    uid = request.form['uid']
    password = request.form['password']

    user = User.query.filter(and_(User.id == uid, User.password == password)).first()
    if user:
        session['uid'] = user._id
        #print session.viewitems()
        #print dir(session)
        return jsonify(code='1', msg='succeed, setting cookies')
    else:
        return jsonify(code='0', msg='failed, invalid user_id or password')


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
        return jsonify(code='0', msg='invalid book id')
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
        return jsonify(code='0', msg='invalid user id')
    else:
        ret = {'uid': user._id, 'id': user.id, 'name': user.username,
               'email': user.email, 'type': user.type}
        return jsonify(**ret)


@app.route('/api/insert_user', methods=['POST'])
def insert_user():
    id = request.form['uid']
    password = request.form['password']

    if User.query.filter(User._id == id).first():
        return jsonify(code='0', msg='failed, this id has been used')

    new_user = User(id, password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(code='1', msg='succeed')


@app.route('/api/insert_book', methods=['POST'])
def insert_book():
    name = request.form['name']
    author = request.form['author']
    description = request.form['description']
    chapter_number = request.form['chapter_number']

    cover = request.files['cover']
    book = request.files['book']

    file_name = datetime.today().strftime('%Y%M%d%H%M%f')
    #print file_name

    cover_name = file_name + '.' +secure_filename(cover.filename).split('.')[-1]
    book_name = file_name + '.' + secure_filename(book.filename).split('.')[-1]

    cover_path = os.path.join(COVER_DIR, cover_name)
    book_path = os.path.join(BOOK_DIR, book_name)

    cover.save(cover_path)
    book.save(book_path)

    new_book = Book(name, 1, chapter_number, '', book_path, author, cover_path, description)
    db.session.add(new_book)
    db.session.commit()

    return jsonify(code='1', msg='insert book succeed')


@app.route('/api/insert_audio', methods=['POST'])
def insert_audio():
    book_id = request.form['book_id']
    chapter_number = request.form['chapter_number']
    description = request.form['description']

    audio = request.files['audio']

    book = Book.query.filter(Book._id == book_id).first()

    if not book:
        return jsonify(code='0', msg='invalid book id')

    if not 0 < int(chapter_number) <= book.chapter_number:
        #print chapter_number
        #print book.chapter_number
        return jsonify(code='0', msg='invalid chapter number')

    file_name = datetime.today().strftime('%Y%M%d%H%M%f')
    audio_name = file_name + '.' +secure_filename(audio.filename).split('.')[-1]

    audio_path = os.path.join(AUDIO_DIR, audio_name)
    audio.save(audio_path)

    new_audio = Audio(audio_path, 1, book_id, chapter_number, description)
    db.session.add(new_audio)
    db.session.commit()

    return jsonify(code='1', msg='insert audio succeed')


@app.route('/api/delete_user', methods=['POST'])
def delete_user():
    user_name = request.form['name']
    password = request.form['password']

    user = User.query.filter(and_(User.id == user_name, User.password == password)).first()

    if not user:
        return jsonify(code='0', msg='invalid user name or password')

    if user.books or user.audios:
        return jsonify(code='0', msg='this user has uploaded files, delete those files first')

    db.session.delete(user)
    db.session.commit()

    return jsonify(code='1', msg='delete user succeed')


@app.route('/api/delete_book', methods=['POST'])
def delete_book():
    book_id = request.form['book_id']

    book = Book.query.filter(Book._id == book_id).first()

    if not book:
        return jsonify(code='0', msg='invalid book id')

    if book.audios:
        return jsonify(code='0', msg='this book has audio files, delete those files first')

    db.session.delete(book)
    db.session.commit()

    os.remove(book.file_url)
    os.remove(book.cover)

    return jsonify(code='1', msg='delete book succeed')


@app.route('/api/delete_audio', methods=['POST'])
def delete_audio():
    audio_id = request.form['id']

    audio = Audio.query.filter(Audio._id == audio_id).first()

    if not audio:
        return jsonify(code='0', msg='invalid audio id')

    db.session.delete(audio)
    db.session.commit()

    os.remove(audio.file_url)

    return jsonify(code='1', msg='delete audio succeed')


@app.route('/api/update_user', methods=['POST'])
def update_user():
    name = request.form['name']
    password = request.form['password']

    new_pass = request.form['new_pass']

    user = User.query.filter(and_(User.id == name, User.password == password))
    if not user:
        return jsonify(code='0', msg='invalid user name')

    user.update({'password': new_pass})
    db.session.commit()

    return jsonify(code='1', msg='succeed update user info')

"""
@app.route('/api/update_book', methods=['POST'])
def update_book():
    author = request.form['author']
    description = request.form['description']
    chapter_number = request.form['chapter_number']

    cover = request.files['cover']
    book = request.files['book']

    file_name = datetime.today().strftime('%Y%M%d%H%M%f')
    #print file_name

    cover_name = file_name + '.' +secure_filename(cover.filename).split('.')[-1]
    book_name = file_name + '.' + secure_filename(book.filename).split('.')[-1]

    cover_path = os.path.join(COVER_DIR, cover_name)
    book_path = os.path.join(BOOK_DIR, book_name)

    cover.save(cover_path)
    book.save(book_path)

    new_book = Book(name, 1, chapter_number, '', book_path, author, cover_path, description)
    db.session.add(new_book)
    db.session.commit()

    return jsonify(code='1', msg='insert book succeed')
"""



