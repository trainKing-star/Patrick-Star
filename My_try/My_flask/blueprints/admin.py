from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app,send_from_directory
from flask_login import login_required,current_user
from My_flask.models import  Admin,Video,Category
from My_flask.forms import  Update_dataForm,VideodeleteForm,PhotoForm,CategoryForm,LoginForm,CategoryForm1,DeleteForm
from My_flask.extensions import  db,Dropzone
from flask_dropzone import random_filename
import os

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/video_see')
@login_required
def video1():
    videos = Video.query.all()
    return render_template('admin/video1.html',videos=videos)

@admin_bp.route('/video_delete',methods=['GET','POST'])
@login_required
def video2():
    form = VideodeleteForm()
    if form.validate_on_submit():
        title = form.title.data
        category_id = form.category.data
        video = Video.query.filter(title==Video.title,category_id==Video.category_id).first()
        db.session.delete(video)
        db.session.commit()
        flash('删除成功')
        return redirect(url_for('admin.video2'))
    return render_template('admin/video2.html',form=form)

@admin_bp.route('/category_manage',methods=['GET','POST'])
@login_required
def category():
    form1 = CategoryForm()
    form2 = CategoryForm1()
    if form1.submit.data and form1.validate_on_submit():
        name = form1.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('admin.category'))
    if form2.submit1.data and form2.validate_on_submit():
        name = form2.name.data
        category = Category.query.filter(name==Category.name).first()
        db.session.delete(category)
        db.session.commit()
        flash('删除成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category.html',form1=form1,form2=form2)


@admin_bp.route('/user_manage',methods=['GET','POST'])
@login_required
def usermanage():
    form = DeleteForm()
    users = Admin.query.all()
    if form.validate_on_submit():
        username = form.username.data
        user = Admin.query.filter(username==Admin.username).first()
        db.session.delete(user)
        db.session.commit()
        flash('注销成功')
        return redirect(url_for('admin.usermanage'))
    return render_template('admin/usermanage.html',users=users,form=form)


@admin_bp.route('/user/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
