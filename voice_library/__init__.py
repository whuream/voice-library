# encoding: utf-8
__author__ = 'SuTong'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///voice_library.db'
app.config['SECRET_KEY'] = 'kamisama'

Bootstrap(app)

db = SQLAlchemy(app)
