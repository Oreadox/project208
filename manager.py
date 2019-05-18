# encoding: utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, api, db
from app.api.user import Token, UserData, Password, Register
from app.api.question import Question, QuestionMessage, MyQuestion, GetSet
from app.api.answer import MyAnswer, AnswerMessage

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# api.add_resource(Token, '/api/user/token')
api.add_resource(UserData, '/api/user/data')
api.add_resource(Password, '/api/user/change')
api.add_resource(Question, '/api/question')
api.add_resource(MyQuestion, '/api/question/my')
api.add_resource(QuestionMessage, '/api/question/message')
api.add_resource(AnswerMessage, '/api/answer/message')
api.add_resource(MyAnswer, '/api/answer/my')
api.add_resource(Register, '/api/user/login')
api.add_resource(GetSet, '/api/getset')

if __name__ == '__main__':
    manager.run()
