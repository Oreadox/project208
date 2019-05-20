# encoding: utf-8
from flask_restful import Resource, request, reqparse, abort
import requests
import json
from .. import db, auth
from ..message import success_msg, fail_msg, add_args
from ..models import DefaultMessage, Answer, QuestionSet
from flask import g


class MyAnswer(Resource):
    @auth.login_required
    def get(self):

        """
        查看我回答的问题
        """
        user = g.user
        answers = Answer.query.filter_by(user_id=user.id).all()
        if answers:
            data = [answer.to_json() for answer in answers]
            return success_msg(msg="获取成功", data=data)
        else:
            return fail_msg(msg="你还没有回答问题")

    @auth.login_required
    def post(self):

        """
        答题
        """
        answer_man = g.user
        args = add_args([
            ["set_id", str, True, ""],
            ["answer", dict, False, ""],
            ["message", str, False, ""]
        ]).parse_args()
        question = QuestionSet.query.filter_by(id=args["set_id"]).first()
        q = json.loads(question.questions.replace("'", '"'))
        score = 0
        for i in q:
            if q[i] == args["answer"][i]:
                score = score + 100 / len(q)
        answer = str(args["answer"])
        answers = Answer(user_id=answer_man.id,
                         set_id=args["set_id"],
                         answers=answer,
                         message=args["message"],
                         score=score)
        db.session.add(answers)
        db.session.commit()
        data = {
            "score": score
        }
        if score >= 60:
            qst_set = QuestionSet.query.filter_by(id=args["set_id"]).first()
            message = qst_set.message
            data['message'] = message
            return success_msg(msg="提交成功", data=data)
        else:
            data['message'] = "由于研究结果未达标准，你无法查看TA给你的小纸条喔～"
            return success_msg(msg="提交成功", data=data)


class AnswerCheck(Resource):
    """检查是否是第二次答题或者自己答自己题"""

    @auth.login_required
    def get(self, id):
        answer_man = g.user
        ans = Answer.query.filter_by(user_id=answer_man.id, set_id=id).first()
        que = QuestionSet.query.filter_by(user_id=answer_man.id, id=id).first()
        if ans:
            return fail_msg(msg="你只能回答一次哦")
        elif que:
            return fail_msg(msg="不能回答自己出的题～")
        return success_msg(msg="")


class AnswerMessage(Resource):
    """默认留言（仅答题者）"""

    @auth.login_required
    def get(self):
        """获取默认留言"""

        messages = DefaultMessage.query.filter_by(angle=2).all()
        data = {
            'total': len(messages),
            'content': [message.content for message in messages]
        }
        return success_msg(msg='获取成功', data=data)
