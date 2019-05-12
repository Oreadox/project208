# encoding: utf-8
from flask_restful import Resource, request, reqparse, abort
import requests
import json
from .. import db, auth
from ..message import success_msg, fail_msg, add_args
from ..models import DefaultQuestion, DefaultMessage, Answer, QuestionSet
from flask import g


class Question(Resource):
    '题目相关'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    @auth.login_required
    def get(self):
        '获取题目数据'
        id = self.parser.parse_args().get('id')
        if not id:  # 获取所有有效的题目内容
            questions = DefaultQuestion.query.filter_by(is_valid=True).all()
            data = {
                'total': len(questions),
                'id': [question.id for question in questions]
            }
            return success_msg(msg='获取成功', data=data)
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


class QuestionMessage(Resource):
    '默认留言（仅出题者）'

    @auth.login_required
    def get(self):
        '获取默认留言'
        filters = {
            DefaultMessage.is_valid is True,
            DefaultMessage.angle != 2
        }
        messages = DefaultMessage.query.filter(*filters).all()
        data = {
            'total': len(messages),
            'content': [message.content for message in messages]
        }
        return success_msg(msg='获取成功', data=data)


class MyQuestion(Resource):
    """
    获取我设置的题目
    """

    @auth.login_required
    def get(self):
        user = g.user
        questions = QuestionSet.query.filter_by(user_id=user.id).all()

        if questions:
            data = []
            for qu in questions:
                all_answer = []
                for ans in qu.answers:
                    answer = {
                        "answer_man": ans.user_id,
                        "answers": json.loads(ans.answers.replace("'", '"')),
                        "time": str(ans.create_time),
                        "score": ans.score

                    }
                    all_answer.append(answer)
                ques = {
                    "set_id": qu.id,
                    "questions": json.loads(qu.questions.replace("'", '"')),
                    "messages": qu.message,
                    "all_answers": all_answer

                    }
                data.append(ques)

            return success_msg(msg="获取成功", data=data)
        else:
            return fail_msg(msg="你还没有设置题目哦")

    @auth.login_required
    def post(self):
        user = g.user
        args = add_args([
            ["questions", dict, True, ""],
            ["messages", str, True, ""]
        ]).parse_args()
        question = str(args["questions"])
        questions = QuestionSet.query.filter_by(user_id=user.id).first()
        if questions:
            return fail_msg(msg="您已经出过题目了")
        questions = QuestionSet(user_id=user.id,
                                questions=question,
                                message=args["messages"])
        db.session.add(questions)
        db.session.commit()
        return success_msg(msg="出题成功！")
