from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required,current_user
from My_flask.models import  Admin,Video
from My_flask.forms import  Update_dataForm,VideoForm,PhotoForm
from My_flask.extensions import  db,Dropzone
from flask_dropzone import random_filename
import os


auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/user/<int:id>')
@login_required
def index(id):
    admin = Admin.query.get(id)
    return render_template('auth/index.html',admin=admin)

@auth_bp.route('/user/<int:id>/update_data',methods=['GET','POST'])
@login_required
def update_data(id):
    form = Update_dataForm()
    if form.validate_on_submit():
        password1 = form.password1.data
        password2 = form.password2.data
        recomment = form.recomment.data
        if password1 == password2:
            admin = Admin.query.get(id)
            admin.password = password1
            admin.recomment = recomment
            db.session.commit()
            flash('修改成功')
            return redirect(url_for('auth.index',id=id))
    return render_template('auth/update_date.html',form=form)

@auth_bp.route('/user/<int:id>/upload_photo',methods=['GET','POST'])
@login_required
def upload_photo(id):
    form = PhotoForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = random_filename(photo.filename)
        photo.save(os.path.join(current_app.config['AVATARS_SAVE_PATH'],filename))
        admin = Admin.query.get(id)
        admin.avatar_l = filename
        db.session.commit()
        return redirect(url_for('auth.index',id=id))
    return render_template('auth/upload_photo.html',form=form)


@auth_bp.route('/user/<int:id>/upload_video',methods=['GET','POST'])
@login_required
def upload_video(id):
    form = VideoForm()
    if form.validate_on_submit():
        title = form.title.data
        category_id = form.category.data
        videoname = form.video.data
        filename = random_filename(videoname.filename)
        videoname.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
        video = Video(title=title,category_id=category_id,videoname=filename,admin_id=id)
        db.session.add(video)
        db.session.commit()
        return redirect(url_for('auth.index',id=id))
    return render_template('auth/upload_video.html',form=form)