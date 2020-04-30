from flask import session,g,Blueprint,request,render_template,redirect,flash,url_for,current_app,jsonify
from catchat.extensions import  db,login_manager,send_mail,Api
from catchat.models  import User,Room,Messager
from flask_login import current_user,login_user,login_required,logout_user
from flask_dropzone import random_filename
from flask_restful import Resource,fields,marshal_with,reqparse
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os


api_bp = Blueprint('api',__name__)
auth = HTTPBasicAuth()
serializer = Serializer('secret key here',expires_in=300)

@auth.verify_password
def verify_password(username,password):
    try:
        data=serializer.loads(g.token)
    except:
        data=None
    if data:
        user = User.query.get(data['id'])
    else:
        user = None
    if not user:
        user = User.query.filter(User.username==username).first()
        if not user or user.password_hash != password:
            return False
        g.token = serializer.dumps({'id':user.id})
        return True
    return True


@api_bp.route('/index')
@auth.login_required
def index():
    return 'login success'

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
        'room_url':room.room_url,
        'description':room.description
    }

def user_resource(user):
    return {
    'id':user.id,
    'username':user.username,
    'password_hash':user.password_hash,
    'telephone':user.telephone,
    'email_hash':user.email_hash,
    'timestamp':user.timestamp,
    'country':user.country,
    'rooms':[user_resource_room(room) for room in user.rooms],
    'messages':[user_resource_message(messager) for messager in user.messages]
    }

def user_resource_list(users):
    return {
        'users':[user_resource(user) for user in users]
    }

post_parser = reqparse.RequestParser()
post_parser.add_argument('username',type=str)
post_parser.add_argument('password_hash',type=str)
post_parser.add_argument('telephone',type=str)
post_parser.add_argument('email_hash',type=str)
post_parser.add_argument('country',type=str)

class User_data(Resource):
    def get(self,userid):
        if userid == 0:
            users = User.query.all()
            return jsonify(user_resource_list(users))
        elif User.query.get(userid):
            return jsonify(user_resource(User.query.get(userid)))
        else:
            return jsonify({'error':'no user'})

    def post(self):
        args = post_parser.parse_args()
        user = User(username=args.username,password_hash=args.password_hash,telephone=args.telephone,email_hash=args.email_hash,country=args.country)
        db.session.add(user)
        db.session.commit()
        return jsonify(user_resource(user))

    def put(self,userid):
        arg = post_parser.parse_args()
        user = User.query.get(userid)
        if arg.username:
            user.username = arg.username
        if arg.password_hash:
            user.password_hash = arg.password_hash
        if arg.telephone:
            user.telephone = arg.telephone
        if arg.email_hash:
            user.email_hash = arg.email_hash
        if arg.country:
            user.country = arg.country
        db.session.commit()
        return jsonify(user_resource(user))

Api.add_resource(User_data,'/api/update/user/<int:userid>','/api/create/user','/api/user/<int:userid>',methods=['GET','POST','PUT'])

def room_resource_list(rooms):
    return {
        'rooms':[room_resource(room) for room in rooms]
    }

def room_resource(room):
    return {
        'roomid':room.id,
        'roomname':room.roomname,
        'room_url':room.room_url,
        'description':room.description,
        'author':{
            'userid':room.author.id,
            'username':room.author.username
        },
        'messagers':[{'messageid':messager.id,'body':messager.body,'m_timestamp':messager.timestamp} for messager in room.messagers]
    }

room_post_parser = reqparse.RequestParser()
room_post_parser.add_argument('roomname',type=str)
room_post_parser.add_argument('topic',type=str)
room_post_parser.add_argument('description',type=str)
room_post_parser.add_argument('author_id',type=int)

class Room_data(Resource):
    def get(self,roomid):
        if roomid == 0:
            return jsonify(room_resource_list(Room.query.all()))
        if Room.query.get(roomid):
            return jsonify(room_resource(Room.query.get(roomid)))
        return jsonify({'error':'no room'})

    def post(self):
        args = room_post_parser.parse_args()
        if not User.query.filter(User.id == args.author_id).first():
            return jsonify({'error':'no user'})
        room = Room(roomname=args.roomname,topic=args.topic,description=args.description,author_id=args.author_id)
        db.session.add(room)
        db.session.commit()
        room.url_room()
        db.session.commit()
        return jsonify(room_resource(room))

    def put(self,roomid):
        if not Room.query.get(roomid):
            return 'no room'
        room = Room.query.get(roomid)
        args = room_post_parser.parse_args()
        if args.roomname:
            room.roomname = args.roomname
        if args.description:
            room.description = args.description
        if args.topic:
            room.topic=args.topic
        if args.author_id:
            room.author_id = args.author_id
        db.session.commit()
        return jsonify(room_resource(room))

Api.add_resource(Room_data,'/api/room/<int:roomid>','/api/create/room','/api/update/room/<int:roomid>',methods=['GET','POST','PUT'])

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
        'roomname':messager.room.roomname
    }
    }

message_post_parser = reqparse.RequestParser()
message_post_parser.add_argument('body',type=str)
message_post_parser.add_argument('room_id',type=int)
message_post_parser.add_argument('auth_id',type=int)

class Message_data(Resource):
    def get(self,messageid):
        if messageid == 0:
            return jsonify(messager_resource_list(Messager.query.all()))
        if Messager.query.get(messageid):
            return jsonify(messager_resource(Messager.query.get(messageid)))
        return jsonify({'error':'no messger'})

    def post(self):
        args = message_post_parser.parse_args()
        messager = Messager(body=args.body)
        if args.room_id:
            messager.room_id = args.room_id
        else:
            return 'no room_id'
        if args.auth_id:
            messager.auth_id = args.auth_id
        else:
            return 'no auth_id'
        db.session.add(messager)
        db.session.commit()
        return jsonify(messager_resource(messager))

    def put(self,messageid):
        if not Messager.query.get(messageid):
            return 'no message'
        messager = Messager.query.get(messageid)
        args = message_post_parser.parse_args()
        if args.body:
            messager.body = args.body
        if args.auth_id:
            messager.auth_id = args.aut_id
        else:
            return 'no auth_id'
        if args.room_id:
            messager.room_id =args.room_id
        else:
            return 'no room_id'
        db.session.commit()
        return jsonify(messager_resource(messager))


Api.add_resource(Message_data,'/api/message/<int:messageid>','/api/create/message','/api/update/message/<int:messageid>',methods=['GET','POST','PUT'])