# encoding: utf-8
__author__ = 'SuTong'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_library.db'
app.config['SECRET_KEY'] = 'kamisama'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_AS_ASCII'] = False


BASE_DIR = os.path.join(os.path.curdir, 'data')
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
BOOK_DIR = os.path.join(BASE_DIR, 'book')
COVER_DIR = os.path.join(BASE_DIR, 'cover')

for dir_name in [AUDIO_DIR, BOOK_DIR, COVER_DIR]:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

Bootstrap(app)

db = SQLAlchemy(app)

from module.audio import Audio
from module.book import Book
from module.user import User

from api import *

