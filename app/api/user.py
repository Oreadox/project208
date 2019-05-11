# encoding: utf-8

from flask_restful import Resource, request, reqparse
from flask import g
import requests
import json
from .. import db, auth
from ..message import success_msg, fail_msg
from ..config import WeChatApiConfig
from ..models import User


class Token(Resource):
    'token相关'

    def post(self):
        '获取token'
        request_data = request.get_json(force=True)
        code = request_data.get('code')
        if not code:
            return fail_msg(status=-101, msg='需要用户登录凭证！')
        payload = {
            'appid': WeChatApiConfig.appid,
            'secret': WeChatApiConfig.appsecret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        r = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token", params=payload)
        user_code = json.loads(r.content.decode())
        if user_code.get('errcode'):
            return fail_msg(status=-102, msg='Code无效')
        user = self.save_data(access_token=user_code.get('access_token'), openid=user_code.get('openid'))
        token = user.generate_auth_token()
        return success_msg(data={'token': token})

    def save_data(self, access_token, openid):
        '保存用户信息'
        payload = {
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }
        r = requests.get("https://api.weixin.qq.com/sns/userinfo", params=payload)
        user_data = json.loads(r.content.decode())
        user = User.query.filter_by(openid=user_data.get('openid')).first()
        if user:
            user.nickname = user_data.get('nickname')
            user.gender = user_data.get('sex')
            user.icon_url = user_data.get('headimgurl')
            db.session.commit()
            return user
        else:
            user = User(nickname=user_data.get('nickname'), gender=user_data.get('sex'),
                        icon_url=user_data.get('headimgurl'))
            db.session.add(user)
            db.session.commit()
            return user


class UserData(Resource):
    '用户信息'

    @auth.login_required
    def get(self):
        '获取用户信息'
        user = "1"
        user_data = {
            'id': user.id,  # 用户id(不是openid)
            'nickname': user.nickname,
            'gender': user.gender,  # 1为男性，2为女性，0为未知
            'icon_url': user.icon_url,  # 用户头像URL,具体见微信官方文档
            'registration_time': str(user.registration_time)
        }
        return success_msg(msg='获取成功', data=user_data)


class TestLogin(Resource):
    '测试用接口'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('code', type=str)
        self.parser.add_argument('state', type=str)

    def get(self):
        data = self.parser.parse_args()
        payload = {
            'appid': WeChatApiConfig.appid,
            'secret': WeChatApiConfig.appsecret,
            'code': data['code'],
            'grant_type': 'authorization_code'
        }
        r = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token", params=payload)
        user_code = json.loads(r.content.decode())
        if user_code.get('errcode'):
            return fail_msg(status=0, msg='Code无效')
        user = self.get_data(access_token=user_code.get('access_token'), openid=user_code.get('openid'))
        return success_msg(data={'user_data': user})

    def get_data(self, access_token, openid):
        '获取用户信息'
        payload = {
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }
        r = requests.get("https://api.weixin.qq.com/sns/userinfo", params=payload)
        user_data = json.loads(r.content.decode())
        user = {}
        user['nickname'] = user_data.get('nickname')
        user['gender'] = user_data.get('sex')
        user['icon_url'] = user_data.get('headimgurl')
        return user
