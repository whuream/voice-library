# encoding: utf-8
__author__ = 'SuTong'

from voice_library import app
from flask import render_template


@app.route('/', methods=['GET'])
def home():
    return render_template('test.html')

