import datetime
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('ARVIZTURO_DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_ECHO = False