# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app,api,db
from app.api.user import Token
from app.models import User, QuestionSet, Answer, DefaultQuestion, DefaultMessage

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

api.add_resource(Token,'/api/user/token')


if __name__ == '__main__':
    manager.run()