# encoding: utf-8
__author__ = 'SuTong'

from seetings import *

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

if PLATFORM == 'sae':
    from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_HOST_S
    from sae.storage import Bucket

app = Flask(__name__)

# debug mode on
app.debug = True

if PLATFORM == 'sae':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s?charset=utf8' \
                                        %(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
elif PLATFORM == 'local':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_library.db'

app.config['SECRET_KEY'] = 'kamisama'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_AS_ASCII'] = False

if PLATFORM == 'local':
    for dir_name in [AUDIODIR, BOOKDIR, COVERDIR]:
        t = os.path.join(BASEDIR, dir_name)
        if not os.path.exists(t):
            os.makedirs(t)

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

