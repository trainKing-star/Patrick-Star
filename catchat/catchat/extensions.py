

from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_mail import Mail
from faker import Faker
from flask_mail import Message
from flask_restful import Api

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
mail = Mail()
faker = Faker('zh_CN')
Api = Api()

def send_mail(subject,to,body):
    message = Message(subject=subject,recipients=[to],body=body)
    mail.send(message)


@login_manager.user_loader
def load_user(user_id):
    from catchat.models import User
    return User.query.get(int(user_id))

login_manager.login_view = 'auth.login'