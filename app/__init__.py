# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api
from flask_cors import CORS
import requests
import json
from .config import FlaskConfig, WeChatApiConfig

app = Flask(__name__)
app.config.from_object(FlaskConfig)
db = SQLAlchemy(app)
auth = HTTPTokenAuth()
api = Api(app)
CORS(app)


@app.after_request
def after_request(resp):
    db.session.close()
    return resp


from .models import User
from flask import g, blueprints




@auth.verify_token
def verify_token(token):
    # if token == 1:
    #     return True
    # else:
    #     user = User.verify_auth_token(token)
    #     if not user:
    #         return False
    #     g.user = user
    #     return True
    user = User.query.filter_by(id=token).first()
    if not user:
        return False
    g.user = user
    return True

