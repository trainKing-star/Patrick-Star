from flask import Blueprint,render_template,redirect,url_for,request,flash,session,jsonify
from flask_socketio import emit,join_room,leave_room,send
from catchat.extensions import *
from catchat.models import User,Room,Messager
from flask_login import current_user,login_user,logout_user,login_required

chat_bp = Blueprint('chat',__name__)


@chat_bp.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


@chat_bp.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password_hash')
        repeatpassword = request.form.get('repeatpassword')
        telephone = request.form.get('telephone')
        email = request.form.get('email_hash')
        country = request.form.get('country')
        if password == repeatpassword:
            user = User(username=username,telephone=telephone,country=country,password_hash=password,email_hash=email)
            db.session.add(user)
            db.session.commit()
            print(user.username)
            #return redirect('/#/access')
            return jsonify({'AAC':'true'},user_resource(user))
        return jsonify({'AAC':'false'})

@chat_bp.route('/login',methods=['POST'])
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password_hash')
        if User.query.filter(username==User.username).first():
            user = User.query.filter(username==User.username).first()
            if user.password_hash == password:
                login_user(user)
                return jsonify({'AAB':'true'},user_resource(user))
            return jsonify({'AAB':'false'})
        return jsonify({'AAB':'false'})


@chat_bp.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'AAD':'true'})


@socketio.on('send_message')
@login_required
def send_message(data):
    message = Messager(body=data,auth_id=current_user.id,room_id=session['room'])
    db.session.add(message)
    db.session.commit()
    emit('send_message',{'message':data,'username':current_user.username,'photo':current_user.photo},room=session['room'])

@socketio.on('connect')
@login_required
def connect():
    user = User.query.get(current_user.id)
    emit('get_username',{'username':user.username})

@socketio.on('join')
@login_required
def join():
    join_room(session['room'])
    emit('send_message',{'data':current_user.username + '进入了房间'},room=session['room'])

@socketio.on('leave')
@login_required
def leave():
    leave_room(session['room'])
    emit('send_message', {'data': current_user.username + '离开了房间'},room=session['room'])





