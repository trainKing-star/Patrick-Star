from flask import Blueprint,request,render_template,redirect,flash,url_for,current_app
from catchat.extensions import  db,login_manager,send_mail
from catchat.models  import User
from flask_login import current_user,login_user,login_required,logout_user
from flask_dropzone import random_filename
import os



auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/')
def index():
    user = User.query.get(current_user.id)
    pass

@auth_bp.route('/updateps',methods=['GET','POST'])
def update():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        password = request.form.get('password')
        repeatpassword = request.form.get('repeatpassword')
        if password == repeatpassword:
            user.hash_password(password)
            db.session.commit()
            return redirect(url_for('auth.index'))
        return redirect(url_for('auth.update'))
    return render_template()

@auth_bp.route('/photo',methods=['GET','POST'])
def photo():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        file = request.files.get('file')
        filename = random_filename(file.filename)
        db.session.commit()
        return redirect(url_for('auth.index'))
    return redirect(url_for('auth.photo'))

@auth_bp.route('/createroom',methods=['GET','POST'])
def create():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        photo = request.form.get('photo')
        name = request.form.get('roomname')
        description = request.form.get('description')
        pass