# encoding: utf-8
__author__ = 'SuTong'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_library.db'
app.config['SECRET_KEY'] = 'kamisama'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

Bootstrap(app)

db = SQLAlchemy(app)

from module.audio import Audio
from module.book import Book
from module.user import User

from api import *

