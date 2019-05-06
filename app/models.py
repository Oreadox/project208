# encoding: utf-8
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime
from app import db
from app.config import FlaskConfig


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.SmallInteger, nullable=False)
    icon_url = db.Column(db.String(256))
    registration_time = db.Column(db.DateTime, default=datetime.now)

    def generate_auth_token(self, expiration=60 * 60 * 24):
        serialize = Serializer(FlaskConfig.SECRET_KEY, expires_in=expiration)
        return serialize.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serialize = Serializer(FlaskConfig.SECRET_KEY)
        try:
            data = serialize.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class QuestionSet(db.Model):
    __tablename__ = 'question_sets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    questions = db.Column(db.String(192), nullable=False)  # 例: {"问题序号1":"答案标号1",...} (json格式)
    message = db.Column(db.Text)    # 留言完整内容
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref='question_sets', foreign_keys=user_id)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    set_id = db.Column(db.Integer, db.ForeignKey('question_sets.id'), nullable=False)  # 题组id
    answers = db.Column(db.String(10), nullable=False)  # 例: A,B,C,D,A (str格式)
    message = db.Column(db.Text)    # 留言完整内容
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref='answers', foreign_keys=user_id)
    question_set = db.relationship('QuestionSet', backref='answers', foreign_keys=set_id)


class DefaultQuestion(db.Model):
    __tablename__ = 'default_questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(64), nullable=False)   # 题目
    option_A = db.Column(db.String(32), nullable=False)
    option_B = db.Column(db.String(32), nullable=False)
    option_C = db.Column(db.String(32), nullable=False)
    option_D = db.Column(db.String(32), nullable=False)
    is_valid = db.Column(db.Boolean, default=True)


class DefaultMessage(db.Model):
    __tablename__ = 'default_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(64), nullable=False)  # 默认留言的内容
    angle = db.Column(db.SmallInteger, nullable=False)  # 0代表共同视角，1代表出题人视角，2则是答题人视角
    is_valid = db.Column(db.Boolean, default=True)
