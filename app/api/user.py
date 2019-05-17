# encoding: utf-8

import requests

from flask_restful import Resource, request, reqparse
from flask import g
import json
from .. import db, auth
from ..message import success_msg, fail_msg, add_args
from ..models import User
from .form.user import SignupForm, LoginForm, ChangePasswordForm


class Token(Resource):
    'token相关'

    def post(self):
        '获取token'
        form = LoginForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User.query.filter_by(username=form.username.data).first() or \
               User.query.filter_by(email=form.username.data).first()
        if not user:
            return fail_msg("该用户不存在！")
        if not user.verify_password(password=form.password.data):
            return fail_msg("密码错误！")
        token = user.generate_auth_token()
        return ({'token': token.decode('ascii')})


class UserData(Resource):
    '用户信息'

    @auth.login_required
    def get(self):
        '获取用户信息'
        user = g.user
        user_data = {
            'id': user.id,  # 用户id(不是openid)
            'username': user.nickname,
            'gender': user.gender,  # 1为男性，2为女性，0为未知
            'registration_time': str(user.registration_time)
        }
        return success_msg(msg='获取成功', data=user_data)

    def post(self):
        '新建用户'
        form = SignupForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = User(username=form.username.data)
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return success_msg()

    @auth.login_required
    def put(self):
        '修改用户信息(除密码)'
        user = g.user
        data = request.get_json(force=True)
        user.gender = data.get('gender') if data.get('gender') else user.gender
        db.session.commit()
        return success_msg()

    @auth.login_required
    def delete(self):
        '删除用户'
        db.session.delete(g.user)
        db.session.commit()
        return success_msg()

class Password(Resource):
    '用户密码'

    @auth.login_required
    def put(self):
        '修改密码(需原密码)'
        form = ChangePasswordForm()
        if not form.validate_on_submit():
            return fail_msg(msg='输入错误！')
        if g.error:
            return g.error
        user = g.user
        user.hash_password(form.password.data)
        db.session.commit()
        return success_msg()


class Register(Resource):
    def post(self):
        args = add_args([
            ["username", str, True, "缺少学号"],
            ["password", str, True, "缺少密码"]

        ], "json").parse_args()

        url_a = "https://os.ncuos.com/api/user/token"

        payload = {
            "username": args["username"],
            "password": args["password"]
        }
        headers = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.11.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "6a2ed635-b844-4488-8923-f3c1968ccaa6,7bf472df-2002-4ad9-bda5-52ce0ebb2fea",
            'Host': "os.ncuos.com",
            'accept-encoding': "gzip, deflate",
            'content-length': "50",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url_a, data=payload, headers=headers)
        if response.json().get("status") == 0:
            return response.json()

        payload = ""
        token = 'passport ' + str(response.json().get("token"))
        headers = {
            'Content-Type': "application/json",
            'Authorization':  token,
            'User-Agent': "PostmanRuntime/7.11.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "4df2b6a0-5600-4468-adc6-6071e6292c31,87f000b6-1fba-453d-8cc1-bcb9db01af53",
            'Host': "os.ncuos.com",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        re = requests.request("GET", "https://os.ncuos.com/api/user/profile/basic", data=payload, headers=headers)
        return {
            "message": str(re.json().get("base_info").get("xh"))
        }




