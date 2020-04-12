from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_socketio import emit
from catchat.extensions import  socketio,mail,db
from catchat.models import  User
from flask_login import login_user,logout_user,login_required

chat_bp = Blueprint('chat',__name__)


@chat_bp.route('/index',methods=['GET','POST'])
@login_required
def index():
    users = User.query.order_by(User.timestamp.desc()).all()
    return render_template('chat/index.html',users=users)


@chat_bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repeatpassword = request.form.get('repeatpassword')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        country = request.form.get('country')
        if password == repeatpassword:
            user = User(username=username,telephone=telephone,country=country)
            user.hash_password(password)
            user.hash_email(email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('chat.login'))
        return redirect(url_for('chat.register'))
    return render_template('auth/register.html')

@chat_bp.route('/',methods=['GET','POST'])
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter(username==User.username).first():
            user = User.query.filter(username==User.username).first()
            if user.verify_password(password):
                login_user(user)
                return redirect(url_for('chat.index'))
            flash('密码错误')
            return redirect(url_for('chat.login'))
        flash('用户不存在')
        return redirect(url_for('chat.login'))
    return render_template('auth/login.html')


@chat_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat.login'))








