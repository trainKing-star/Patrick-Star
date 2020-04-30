

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

login_manager.login_view = 'chat.index'

def user_resource_message(messager):
    return {
        'messageid':messager.id,
        'body':messager.body,
        'm_timestamp':messager.timestamp
    }

def user_resource_room(room):
    return {
        'roomid':room.id,
        'roomname':room.roomname,
        'topic':room.topic,
        'room_url':room.room_url,
        'description':room.description
    }

def user_resource(user):
    return {
    'id':user.id,
    'username':user.username,
    'password_hash':user.password_hash,
    'userphoto':user.photo,
    'telephone':user.telephone,
    'email_hash':user.email_hash,
    'timestamp':user.timestamp,
    'country':user.country,
    'rooms':[user_resource_room(room) for room in user.rooms],
    'messages':[user_resource_message(messager) for messager in user.messages]
    }

def room_resource_list(rooms):
    return {
        'rooms':[room_resource(room) for room in rooms]
    }

def room_resource(room):
    return {
        'roomid':room.id,
        'roomname':room.roomname,
        'room_url':room.room_url,
        'topic':room.topic,
        'description':room.description,
        'roomphoto':room.photo,
        'author':{
            'userid':room.author.id,
            'username':room.author.username
        },
        'messagers':[{'messageid':messager.id,'body':messager.body,'m_timestamp':messager.timestamp} for messager in room.messagers]
    }

def messager_resource_list(messagers):
    return {
        'messagers':[messager_resource(messager) for messager in messagers ]
    }

def messager_resource(messager):
    return {
    'messageid':messager.id,
    'body':messager.body,
    'm_timestamp':messager.timestamp,
    'auth_id':{
        'userid':messager.author.id,
        'username':messager.author.username
    },
    'room':{
        'roomid':messager.room.id,
        'roomname':messager.room.roomname,
    }
    }