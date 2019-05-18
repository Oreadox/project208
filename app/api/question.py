# encoding: utf-8
from flask_restful import Resource, request, reqparse, abort
import requests
import json
from .. import db, auth
from ..message import success_msg, fail_msg, add_args
from ..models import DefaultQuestion, DefaultMessage, Answer, QuestionSet
from flask import g


class Question(Resource):
    """题目相关"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)

    @auth.login_required
    def get(self):
        """获取题目数据"""
        id = self.parser.parse_args().get('id')
        if not id:  # 获取所有有效的题目内容
            questions = DefaultQuestion.query.all()
            data = []
            for q in questions:
                data.append(q.to_json())
            return success_msg(msg="成功", data=data)

        question = DefaultQuestion.query.filter_by(id=id).first()
        options = []
        options.append(question.option_A)
        options.append(question.option_B)
        options.append(question.option_C)
        options.append(question.option_D)
        question_data = {
            'id': id,
            'question': question.subject,  # 题目问题
            'options': options
        }
        return success_msg(msg='获取成功', data=question_data)


class QuestionMessage(Resource):
    """获取出题者的默认留言"""

    @auth.login_required
    def get(self):
        messages = DefaultMessage.query.filter_by(angle=1).all()
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
                        "answer_man": ans.user.id,
                        "name": ans.user.name,
                        "sex": ans.user.gender,
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


class GetSet(Resource):
    @auth.login_required
    def get(self, id):
        question = QuestionSet.query.filter_by(id=id).first()
        if not question:
            return fail_msg(msg="没有此题组哦～")
        question_id = json.loads(question.questions.replace("'", '"'))
        datas = []
        for key in question_id.keys():
            qu = DefaultQuestion.query.filter_by(id=key).first()
            data = qu.to_json()
            datas.append(data)
        return success_msg(msg="成功！", data=datas)
        # return {
        #     "a":question_id
        # }






