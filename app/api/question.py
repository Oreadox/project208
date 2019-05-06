# encoding: utf-8
from flask_restful import Resource, request, reqparse, abort
import requests
import json
from .. import db, auth
from ..message import success_msg, fail_msg
from ..models import DefaultQuestion


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
            'option_D': question.option_D,  # D选项内容
        }
        return success_msg(msg='获取成功', data=question_data)


class ValidQuestion(Resource):
    '有效的题目（is_valid==True)'

    @auth.login_required
    def get(self):
        '获取有效的题目内容'
        questions = DefaultQuestion.query.filter_by(is_valid=True)
        data = {
            'total': len(questions),
            'id': [question.id for question in questions]
        }
        return success_msg(msg='获取成功', data=data)
