# encoding: utf-8
__author__ = 'SuTong'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.bootstrap import Bootstrap
from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_HOST_S
import os
from sae.storage import Bucket

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s?charset=utf8' \
                                        %(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
app.config['SECRET_KEY'] = 'kamisama'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_AS_ASCII'] = False

BASE_DIR = 'data'
AUDIO_DIR = 'audio'
BOOK_DIR = 'book'
COVER_DIR = 'cover'

"""
BASE_DIR = os.path.join(os.path.curdir, 'data')
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
BOOK_DIR = os.path.join(BASE_DIR, 'book')
COVER_DIR = os.path.join(BASE_DIR, 'cover')

for dir_name in [AUDIO_DIR, BOOK_DIR, COVER_DIR]:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
"""
#Bootstrap(app)

class nullpool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, apps, info, options):
        super(nullpool_SQLAlchemy, self).apply_driver_hacks(apps, info, options)
        from sqlalchemy.pool import NullPool
        options['poolclass'] = NullPool
        del options['pool_size']

db = nullpool_SQLAlchemy(app)

from module.audio import Audio
from module.book import Book
from module.user import User

from api import *

