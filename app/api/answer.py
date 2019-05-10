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
        answers = Answer.query.filter_by(user=user).all
        if answers:
            data = [answer.to_json() for answer in answers]
            return success_msg(msg="获取成功", data=data)
        else:
            return fail_msg(msg="你还没有回答问题")

    def post(self):

        """
        答题
        """
        answer_man = g.user
        args = add_args([
            ["user_id", str, True, ""],
            ["set_id", str, True, ""],
            ["answer", dict, True, ""],
            ["message", str, True, ""]
        ]).parse_args()
        answer = str(args["answer"])
        answers = Answer(user_id=args["user_id"],
                         set_id=args["set_id"],
                         answer=answer,
                         message=args["message"],
                         user=answer_man)
        db.session.add(answers)
        db.commit()
        qst_set = QuestionSet.query.filter_by(user_id=args["user_id"])
        data = qst_set.message
        return success_msg(msg="提交成功", data=data)





