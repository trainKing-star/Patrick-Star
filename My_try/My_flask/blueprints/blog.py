from flask import Blueprint, render_template, url_for, flash, redirect, send_from_directory, current_app
from flask_login import login_user,logout_user,login_required,current_user
from My_flask.models import  Admin,Category,Video,Comment
from My_flask.forms import  LoginForm,RegisterForm,CommentForm
from My_flask.extensions import  db

blog_bp = Blueprint('blog',__name__,template_folder='templates')

@blog_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('blog/index.html',categories=categories)

@blog_bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        rememeber = form.remember.data
        if Admin.query.filter(username==Admin.username).first():
            admin = Admin.query.filter(username==Admin.username).first()
            if username == admin.username and password == admin.password:
                login_user(admin,rememeber)
                flash('欢迎回来')
                return redirect(url_for('blog.index'))
            flash('用户名或者密码错误')
        else:
            flash('无用户')
    return render_template('blog/login.html',form=form)

@blog_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('blog.index'))

@blog_bp.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        if Admin.query.filter(username==Admin.username).first():
            flash('用户已存在')
            return redirect(url_for('blog.register'))
        if password1==password2:
            admin = Admin(username=username,password=password1)
            db.session.add(admin)
            db.session.commit()
            flash('注册成功')
            return redirect(url_for('blog.login'))
    return render_template('blog/register.html',form=form)

@blog_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    print(current_app.config['AVATARS_SAVE_PATH'])
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)


@blog_bp.route('/admin_login',methods=['GET','POST'])
def adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if Admin.query.filter(username==Admin.username,password==Admin.password).first():
            admin = Admin.query.filter(username==Admin.username,password==Admin.password).first()
            login_user(admin)
            return redirect(url_for('admin.index'))
        flash('用户不存在')
        return redirect(url_for('blog.adminlogin'))
    return render_template('admin/login.html',form=form)

@blog_bp.route('/videosee/<int:id>',methods=['GET','POST'])
def videosee(id):
    video = Video.query.get(id)
    form = CommentForm()
    if form.validate_on_submit():
        body = form.body.data
        comment = Comment(body=body,video_id=id,admin_id= current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.videosee',id=id))
    return render_template('blog/video.html',video=video,form=form)

@blog_bp.route('/replied/<int:id>',methods=['GET','POST'])
def replied(id):
    form = CommentForm()
    if form.validate_on_submit():
        body = form.body.data
        comment = Comment(body=body,admin_id= current_user.id,replied_id=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.videosee',id=id))
    return render_template('blog/replied.html',form=form)


