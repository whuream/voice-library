__author__ = 'SuTong'

import os

# constants

# 'sae' or 'local'
PLATFORM = 'local'

BASEDIR = 'data'
BUCKET_NAME = 'data'

BOOKDIR = 'book'
AUDIODIR = 'audio'
COVERDIR = 'cover'

if PLATFORM == 'local':
    # IP
    FILE_BASE_URL = 'http://127.0.0.1:5000/'
    FILE_BASE_DIR = os.path.abspath(os.path.curdir)