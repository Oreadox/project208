# encoding: utf-8
from flask_restful import reqparse

def add_args(li, location='json'):
    """add resource reqparse argument from list"""

    res = reqparse.RequestParser()
    for s in li:
        res.add_argument(s[0],
                         type=s[1],
                         required=s[2],
                         help=s[3],
                         location=location)
    return res


def fail_msg(msg, status=0):
    message = {
        "status": status,
        "message": msg
    }
    return message


def success_msg(msg='成功！', status=1, data={}):
    message = {
        "status": status,
        "message": msg
    }
    if data: message['data'] = data
    return message