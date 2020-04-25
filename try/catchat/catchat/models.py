from catchat.extensions import  db
from datetime import datetime
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True)
    password_hash = db.Column(db.String)
    photo = db.Column(db.String,default='imgbase.png')
    telephone = db.Column(db.String,unique=True)
    email_hash = db.Column(db.String,unique=True)
    country = db.Column(db.String,default=None)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    messages = db.relationship('Messager',back_populates='author',cascade='all')
    rooms = db.relationship('Room',back_populates='author',cascade='all')

    def hash_password(self,password):
        self.password_hash = pwd_context.encrypt(password)

    def hash_email(self,email):
        self.email_hash = pwd_context.encrypt(email)

    def verify_password(self,password):
        return pwd_context.verify(password,self.password_hash)

    def verify_email(self,email):
        return pwd_context.verify(email,self.email_hash)

class Tourist(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True)

class Room(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    roomname = db.Column(db.String,unique=True)
    room_url = db.Column(db.String)
    photo = db.Column(db.String)
    topic = db.Column(db.String)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',back_populates='rooms')
    messagers = db.relationship('Messager',back_populates='room',cascade='all')

    def url_room(self):
        self.room_url = 'http://127.0.0.1:5000/room/id=' + str(self.id)

class Messager(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    auth_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',back_populates='messages')
    room_id = db.Column(db.Integer,db.ForeignKey('room.id'))
    room = db.relationship('Room',back_populates='messagers')