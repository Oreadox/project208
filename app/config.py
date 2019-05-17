# encoding: utf-8

import os


class FlaskConfig():
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "S83rQ53gC4vdarcIAvY89Ky4"
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'ncu'
    USERNAME = 'root'
    PASSWORD = 'keyu0102'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_MAX_OVERFLOW = 50
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False


class WeChatApiConfig():
    # appid = os.environ.get('appid')
    # appsecret = os.environ.get('appsecret')
    appid = 'wxf41bc95f18746664'  # WZB 的测试号
    appsecret = '744bf227cd9bed816ae53d7d62b806c9'  # WZB
