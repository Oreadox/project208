# encoding: utf-8

import os

class FlaskConfig():
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "S83rQ53gC4vdarcIAvY89Ky4"
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'db1'
    USERNAME = 'user'
    PASSWORD = 'user'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_MAX_OVERFLOW = 50
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 465 or 994
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = os.environ.get('MAIL_SUBJECT_PREFIX') or 'none'
    MAIL_SENDER = MAIL_USERNAME
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False