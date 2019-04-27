# encoding: utf-8

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