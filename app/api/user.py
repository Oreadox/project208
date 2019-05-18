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
        ]).parse_args()
        user = User.query.filter_by(id=args["username"]).first()
        if user:
            if user.verify_password(password=args["password"]):

                token = user.generate_auth_token()
                return {
                    "status": 1,
                    "message": "登录成功！",
                    "token": token.decode("ascii")
                 }
            return {
                "status": 0,
                "message": "密码错误！"
            }
        urla = "https://os.ncuos.com/api/user/token"
        payload = {
            "username": args["username"],
            "password": args["password"]
        }
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Postman-Token': "1059212e-3f28-4244-9a47-c689158a469e",
            'Host': "os.ncuos.com"
        }

        response = requests.request("POST", urla, data=json.dumps(payload), headers=headers)
        if response.json().get('status') == 0:
            return response.json()
        urlb = "https://os.ncuos.com/api/user/profile/basic"
        token = 'passport ' + response.json().get("token")

        headers = {
            'Content-Type': "application/json",
            'Authorization': token,
            'Cache-Control': "no-cache",
            'Postman-Token': "2a54dde4-15d9-4715-9d59-1ec0a1b6985c"
        }

        re = requests.request("GET", urlb, data='', headers=headers)
        user = User(id=args["username"], name=re.json().get("base_info").get("xm"))
        user.hash_password(args["password"])
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(id=args["username"]).first()
        token = user.generate_auth_token()
        return {
            "status": 1,
            "message": "成功",
            "token": token.decode("ascii")
        }





