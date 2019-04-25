# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail
from .config import FlaskConfig

db = SQLAlchemy()
auth = HTTPTokenAuth()
api = Api()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)
    db.init_app(app)
    mail.init_app(app)
    api.init_app(app)
    CORS(app)
    app = init_app(app)
    return app


def init_app(app):
    @app.after_request
    def after_request(resp):
        db.session.close()
        return resp

    return app


from .models import User
from flask import g


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
