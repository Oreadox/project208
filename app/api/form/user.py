# encoding: utf-8
###此文件仅用于表单/json数据验证
from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, Regexp, EqualTo, DataRequired
from app.models import User
from app.message import fail_msg


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 32),
                                                   Regexp('^[A-Za-z0-9\\u4e00-\u9fa5_]+$', 0,
                                                          '不能输入特殊字符(除下划线)')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 32), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 32),
                                                     Regexp('^[A-Za-z0-9_]+$', 0,
                                                            '不能输入中文及特殊字符(除下划线)')])
    password2 = StringField('Password2', validators=[DataRequired(), EqualTo('password')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            g.error = fail_msg(msg='该邮箱已被注册！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            g.error = fail_msg(msg='该用户已存在！')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 32)])
    password = StringField('Password', validators=[DataRequired(), Length(1, 32)])

    def validate_username(self, field):
        if not (User.query.filter_by(email=field.data).first()
                and User.query.filter_by(username=field.data).first()):
            g.form_error = fail_msg(msg='该用户不存在！')


class ChangePasswordForm(FlaskForm):
    old_password = StringField('Old_password', validators=[DataRequired(), Length(1, 32)])
    new_password = StringField('New_password', validators=[DataRequired(), Length(1, 32)])
    new_password2 = StringField('New_password2word', validators=[DataRequired(), Length(1, 32), EqualTo(new_password)])

    def validate_old_password(self, field):
        if not g.user.verify_password(field):
            g.error = fail_msg(msg='密码错误！')


class ForgetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 32),
                                                   Regexp('^[A-Za-z0-9\\u4e00-\u9fa5_]+$', 0,
                                                          '不能输入特殊字符(除下划线)')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 32), Email()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            g.error = fail_msg(msg='该用户不存在！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            g.error = fail_msg(msg='该用户不存在！')
