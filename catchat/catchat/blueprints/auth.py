from flask import Blueprint,request,render_template,redirect,flash,url_for,current_app
from catchat.extensions import  db,login_manager,send_mail
from catchat.models  import User,Room
from flask_login import current_user,login_user,login_required,logout_user
from flask_dropzone import random_filename
import os



auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/index')
@login_required
def index():
    return render_template('profile.html')

@auth_bp.route('/updateps',methods=['POST'])
@login_required
def update():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = random_filename(file.filename)
            user.photo = filename
            file.save(current_app.config['AVATARS_SAVE_PATH'],filename)
        username = request.form.get('username')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        user.username = username
        user.telephone = telephone
        user.hash_email(email)
        db.session.commit()
        return redirect(url_for('auth.index'))


@auth_bp.route('/createroom',methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = random_filename(file.filename)
            photo = filename
            file.save(current_app.config['AVATARS_SAVE_PATH'], filename)
        name = request.form.get('roomname')
        description = request.form.get('description')
        password = request.form.get('roompassword')
        room = Room(roomname=name,description=description,author_id=current_user.id,roompassword=password)
        db.session.add(room)
        db.session.commit()
        room.url_room()
        db.session.commit()
        return redirect(url_for('chat.chatroom',roomid=room.id))
    return render_template('creategroup.html')

@auth_bp.route('/search',methods=['GET','POST'])
@login_required
def search():
    url =request.form.get('room_url')
    room = Room.query.filter(Room.room_url==url).first()
    if room:
        return redirect(url_for('chat.chatroom',roomid=room.id))
    flash('无房间')
    return redirect('auth.index')