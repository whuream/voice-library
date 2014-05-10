# encoding: utf-8
__author__ = 'SuTong'

from voice_library import *
from flask import request, session, jsonify, send_file
from sqlalchemy.sql.expression import and_
import os
from datetime import datetime
from werkzeug.utils import secure_filename


def save_file(file_name, f):
    if PLATFORM == 'sae':
        bucket = Bucket(BUCKET_NAME)
        bucket.put()
        bucket.put_object(file_name, f)
    elif PLATFORM == 'local':
        f.save(os.path.join(FILE_BASE_DIR, BASEDIR, file_name))


def get_file_url(file_name):
    if PLATFORM == 'sae':
        bucket = Bucket(BUCKET_NAME)
        bucket.put()
        return bucket.generate_url(file_name)
    else:
        return FILE_BASE_URL + BASEDIR + '/' + file_name


def delete_file(path):
    if PLATFORM == 'sae':
        bucket = Bucket(BUCKET_NAME)
        bucket.put()
        bucket.delete_object(path)
    else:
        os.remove(os.path.join(BASEDIR, path))


@app.route('/%s/<path:file_name>' % BASEDIR, methods=['GET'])
def get_file(file_name):
    path = os.path.join(FILE_BASE_DIR, BASEDIR, file_name)
    print path
    return send_file(path)


@app.route('/api/verify_user', methods=['POST'])
def verify_user():
    print os.path.abspath(os.path.curdir)
    id = request.form['id']
    password = request.form['password']

    user = User.query.filter(and_(User.id == id, User.password == password)).first()
    if user:
        session['uid'] = user._id

        return jsonify(code='1', msg='succeed, setting cookies')
    else:
        return jsonify(code='0', msg='failed, invalid user_id or password')


@app.route('/api/logout', methods=['GET'])
def logout():
    session['uid'] = None
    return jsonify(code='1', msg='succeed, cleaning cookies')


@app.route('/api/get_book_list', methods=['GET'])
def get_book_list():
    books = Book.query.all()
    book_list = []
    ret = {'book': book_list}
    for book in books:
        d = {'name': book.name,
             'author': book.author,
             'cover': get_file_url(book.cover),
             'content': book.content,
             'file_url': get_file_url(book.file_url),
             'description': book.description,
             'chapter_number': book.chapter_number,
             'date': book.date}
        # TODO add uploader 's id here
        ret['book'].append(d)

    return jsonify(**ret)


@app.route('/api/get_book_info', methods=['POST'])
def get_book_info():
    book_name = request.form['book_name']

    book = Book.query.filter(Book.name == book_name).first()

    if not book:
        return jsonify(code='0', msg='invalid book id')

    else:
        audio_list = []
        ret = {'audio': audio_list}

        for audio in book.audios:
            d = {'file_url': get_file_url(audio.file_url),
                 'description': audio.description,
                 'chapter_number': audio.chapter_number,
                 'user_id': audio.user_id,
                 'audio_id': audio._id}
            ret['audio'].append(d)

        return jsonify(**ret)


@app.route('/api/get_user_info', methods=['POST'])
def get_user_info():
    id = request.form['id']
    user = User.query.filter(User.id == id).first()

    if not user:
        return jsonify(code='0', msg='invalid user id')

    else:
        ret = {'name': user.username,
               'email': user.email, 'type': user.type}
        return jsonify(**ret)


@app.route('/api/insert_user', methods=['POST'])
def insert_user():
    id = request.form['id']
    password = request.form['password']

    if User.query.filter(User.id == id).first():
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

    c_book = Book.query.filter(Book.name == name).first()
    if c_book:
        return jsonify(code='0', msg='this book name has been used')

    file_name = datetime.today().strftime('%Y%m%d%H%M%S%f')

    cover_path = os.path.join(COVERDIR, file_name + '.' + secure_filename(cover.filename).split('.')[-1])\
        if cover else ''
    book_path = os.path.join(BOOKDIR, file_name + '.' + secure_filename(book.filename).split('.')[-1])\
        if book else ''

    if cover_path:
        save_file(cover_path, cover)

    if book_path:
        save_file(book_path, book)

    new_book = Book(name, 1, chapter_number, '', book_path, author, cover_path, description)
    db.session.add(new_book)
    db.session.commit()

    return jsonify(code='1', msg='insert book succeed')


@app.route('/api/insert_audio', methods=['POST'])
def insert_audio():
    book_name = request.form['book_name']
    chapter_number = request.form['chapter_number']
    description = request.form['description']

    audio = request.files['audio']

    book = Book.query.filter(Book.name == book_name).first()

    if not book:
        return jsonify(code='0', msg='invalid book id')

    if not (0 < int(chapter_number) <= book.chapter_number):
        return jsonify(code='0', msg='invalid chapter number')

    file_name = datetime.today().strftime('%Y%m%d%H%M%S%f')

    audio_path = os.path.join(AUDIODIR, file_name + '.' +secure_filename(audio.filename).split('.')[-1])\
        if audio else ''

    if audio_path:
        save_file(audio_path, audio)

    new_audio = Audio(audio_path, 1, book._id, chapter_number, description)

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
    book_name = request.form['book_name']

    book = Book.query.filter(Book.name == book_name).first()

    if not book:
        return jsonify(code='0', msg='invalid book name')

    if book.audios:
        return jsonify(code='0', msg='this book has audio files, delete those files first')

    db.session.delete(book)
    db.session.commit()

    if book.file_url:
        delete_file(book.file_url)
    if book.cover:
        delete_file(book.cover)

    return jsonify(code='1', msg='delete book succeed')


@app.route('/api/delete_audio', methods=['POST'])
def delete_audio():
    audio_id = request.form['id']

    audio = Audio.query.filter(Audio._id == audio_id).first()

    if not audio:
        return jsonify(code='0', msg='invalid audio id')

    db.session.delete(audio)
    db.session.commit()

    if audio.file_url:
        delete_file(audio.file_url)

    return jsonify(code='1', msg='delete audio succeed')


@app.route('/api/update_user', methods=['POST'])
def update_user():
    name = request.form['name']
    password = request.form['password']

    new_pass = request.form['new_pass']

    user = User.query.filter(and_(User.id == name, User.password == password))
    if not user.first():
        return jsonify(code='0', msg='invalid user name')

    user.update({'password': new_pass})
    db.session.commit()

    return jsonify(code='1', msg='succeed update user info')


@app.route('/api/update_book', methods=['POST'])
def update_book():
    name = request.form['name']
    new_name = request.form['new_name']
    author = request.form['author']
    description = request.form['description']
    chapter_number = request.form['chapter_number']

    cover = request.files['cover']
    book = request.files['book']

    c_book = Book.query.filter(Book.name == name)
    if not c_book.first():
        return jsonify(code='0', msg='invalid book name')

    #if chapter_number < c_book.first().chapter_number:
    #    return jsonify(code='0', msg='chapter number error')

    d = {'name': new_name, 'author': author, 'description': description,
         'chapter_number': chapter_number}

    file_name = datetime.today().strftime('%Y%m%d%H%M%S%f')

    cover_path = os.path.join(COVERDIR, file_name + '.' + secure_filename(cover.filename).split('.')[-1])\
        if cover else ''

    book_path = os.path.join(BOOKDIR, file_name + '.' + secure_filename(book.filename).split('.')[-1])\
        if book else ''

    if c_book.first().cover:
        delete_file(c_book.first().cover)

    if c_book.first().file_url:
        delete_file(c_book.first().file_url)

    if cover_path:
        save_file(cover_path, cover)

        d['cover'] = cover_path

    if book_path:
        save_file(book_path, book)

        d['file_url'] = book_path

    c_book.update(d)
    db.session.commit()

    return jsonify(code='1', msg='update book succeed')


@app.route('/api/update_audio', methods=['POST'])
def update_audio():
    audio_id = request.form['audio_id']
    chapter_number = request.form['chapter_number']
    description = request.form['description']

    audio = request.files['audio']

    c_audio = Audio.query.filter(Audio._id == audio_id)

    if not c_audio:
        return jsonify(code='0', msg='invalid audio id')

    book = c_audio.first().book

    if not 0 < int(chapter_number) <= book.chapter_number:
        return jsonify(code='0', msg='invalid chapter number')

    d = {'chapter_number': chapter_number, 'description': description}

    file_name = datetime.today().strftime('%Y%m%d%H%M%S%f')
    audio_path = os.path.join(AUDIODIR, file_name + '.' +secure_filename(audio.filename).split('.')[-1])\
        if audio else ''

    if c_audio.first().file_url:
        delete_file(c_audio.first().file_url)

    if audio_path:
        save_file(audio_path, audio)
        d['file_url'] = audio_path

    c_audio.update(d)
    db.session.commit()

    return jsonify(code='1', msg='update audio succeed')


@app.route('/api/init_db', methods=['GET'])
def create_db():
    db.create_all()
    kami = User('-', '-', 'kami', 'admin')
    db.session.add(kami)
    db.session.commit()

    kami = User.query.first()

    book1 = Book(u'吃药手册', kami._id)
    book2 = Book(u'治病指南', kami._id)

    audio1 = Audio('', kami._id, 1)
    audio2 = Audio('', kami._id, 2)

    for k in [book1, book2, audio1, audio2]:
        db.session.add(k)

    db.session.commit()

    return 'ok'
