from flask import Blueprint,render_template,redirect,url_for,request,flash,session
from flask_socketio import emit,join_room,leave_room,send
from catchat.extensions import mail,db,socketio
from catchat.models import  User,Room
from flask_login import current_user,login_user,logout_user,login_required

chat_bp = Blueprint('chat',__name__)


@chat_bp.route('/',methods=['GET','POST'])
def index():
    return render_template('access.html')


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
            user = User(username=username,telephone=telephone,country=country)
            user.hash_password(password)
            user.hash_email(email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('chat.index'))
        return redirect(url_for('chat.index'))

@chat_bp.route('/login',methods=['POST'])
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password_hash')
        if User.query.filter(username==User.username).first():
            user = User.query.filter(username==User.username).first()
            if user.verify_password(password):
                login_user(user)
                return redirect(url_for('auth.index'))
            flash('密码错误')
            return redirect(url_for('chat.index'))
        flash('用户不存在')
        return redirect(url_for('chat.index'))
    return redirect(url_for('chat.index'))


@chat_bp.route('/chatroom/<int:roomid>',methods=['GET','POST'])
@login_required
def chatroom(roomid):
    session['room']=roomid
    room =Room.query.get(roomid)
    return render_template('chat.html',room=room)


@chat_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.login'))


@socketio.on('message')
def message(data):
    print(session['room'])
    emit('message',{'data':data},room=session['room'])

@socketio.on('connect')
def connect():
    emit('message',{'data':'连接成功'})

@socketio.on('join')
def join():
    join_room(session['room'])
    emit('message',{'data':current_user.username + '进入了房间'},room=session['room'])

@socketio.on('leave')
def leave():
    leave_room(session['room'])
    emit('message', {'data': current_user.username + '离开了房间'}, room=session['room'])





