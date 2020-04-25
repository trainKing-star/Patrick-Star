from flask import Blueprint,request,render_template,redirect,flash,url_for,current_app,jsonify,session
from catchat.extensions import  *
from catchat.models  import User,Room
from flask_login import current_user,login_user,login_required,logout_user
from flask_dropzone import random_filename
import os



auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/updates',methods=['POST'])
@login_required
def update():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file.filename = 'user_' + str(user.id)  + os.path.splitext(file.filename)[1]
            user.photo = file.filename
            file.save(os.path.join(current_app.config['AVATARS_SAVE_PATH'],file.filename))
        username = request.form.get('username')
        if username:
            user.username = username
        telephone = request.form.get('telephone')
        if telephone:
            user.telephone = telephone
        email = request.form.get('email')
        if email:
            user.email_hash = email
        db.session.commit()
        return jsonify(user_resource(user))


@auth_bp.route('/createroom',methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('roomname')
        description = request.form.get('description')
        topic =request.form.get('topic')
        room = Room(roomname=name,description=description,author_id=current_user.id,topic=topic)
        db.session.add(room)
        db.session.commit()
        room.url_room()
        file = request.files.get('file')
        file.filename = 'room_' + str(room.id)  + os.path.splitext(file.filename)[1]
        file.save(os.path.join(current_app.config['AVATARS_SAVE_PATH'], file.filename))
        room.photo = file.filename
        db.session.commit()
        session['room']=room.id
        return jsonify(room_resource(room))

@auth_bp.route('/search',methods=['GET','POST'])
@login_required
def search():
    url =request.args.get('room_url_user')
    room = Room.query.filter(Room.room_url==url).first()
    if room:
        session['room']=room.id
        return jsonify(room_resource(room))
    user = User.query.filter(User.username==url).first()
    if user:
        return jsonify(user_resource(user))
    return jsonify({'error':'no information'})

@auth_bp.route('/updateroom',methods=['POST'])
@login_required
def updateroom():
    room=Room.query.get(session['room'])
    file = request.files.get('file')
    file.filename = 'room_' + str(room.id) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(current_app.config['AVATARS_SAVE_PATH'], file.filename))
    room.photo=file.filename
    room.roomname=request.form.get('roomname')
    room.description=request.form.get('description')
    room.topic=request.form.get('topic')
    db.session.commit()
    return jsonify(room_resource(room))