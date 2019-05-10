# encoding: utf-8
from flask_restful import Resource, request, reqparse, abort
import requests
import json
from .. import db, auth
from ..message import success_msg, fail_msg
from ..models import DefaultQuestion, DefaultMessage, Answer
from flask import g


class Question(Resource):
    '题目相关'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    @auth.login_required
    def get(self):
        '获取单个题目数据'
        id = self.parser.parse_args().get('id')
        if not id:
            abort(404)
            return None
        question = DefaultQuestion.query.filter_by(id=id).first()
        if not question:
            abort(404)
            return None
        question_data = {
            'id': id,
            'subject': question.subject,  # 题目问题
            'option_A': question.option_A,  # A选项内容
            'option_B': question.option_B,  # B选项内容
            'option_C': question.option_C,  # C选项内容
            'option_D': question.option_D  # D选项内容
        }
        return success_msg(msg='获取成功', data=question_data)


class ValidQuestion(Resource):
    '有效的题目（is_valid==True)'

    @auth.login_required
    def get(self):
        '获取有效的题目内容'
        questions = DefaultQuestion.query.filter_by(is_valid=True).all()
        data = {
            'total': len(questions),
            'id': [question.id for question in questions]
        }
        return success_msg(msg='获取成功', data=data)


class QuestionMessage(Resource):
    '默认留言（仅出题者）'

    @auth.login_required
    def get(self):
        '获取默认留言'
        filters = {
            DefaultMessage.is_valid == True,
            DefaultMessage.angle != 2
        }
        messages = DefaultMessage.query.filter(*filters).all()
        data = {
            'total': len(messages),
            'content': [message.content for message in messages]
        }
        return success_msg(msg='获取成功', data=data)


class MyQuestion(Resource):
    @auth.login_required
    def get(self):
        user = g.user
        answers = Answer.query.filter_by(user_id=user).all()
        if answers:
            data = [answer.to_json() for answer in answers]
            return success_msg(msg="获取成功", data=data)
        else:
            return fail_msg(msg="你还没有设置题目哦")

