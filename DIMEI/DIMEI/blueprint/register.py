from DIMEI.extensions import *
from DIMEI.models import School,Teachar,Student,Grade,Course
from flask import render_template,Blueprint,request,jsonify,url_for,send_from_directory,current_app
import os

register_bp = Blueprint('register',__name__)


@register_bp.route('/school',methods=['POST'])
def school():
    name = request.form.get('name')
    school = School(name=name)
    db.session.add(school)
    db.session.commit()
    return jsonify({'event':'success'},search_school(school))

@register_bp.route('/grade',methods=['POST'])
def grade():
    school_name = request.form.get('school_name')
    name = request.form.get('name')
    grade = Grade(name=name)
    grade.search_school(school_name)
    db.session.add(grade)
    db.session.commit()
    return jsonify({'event':'true'},search_grade(grade))

@register_bp.route('/course',methods=['POST'])
def course():
    subject = request.form.get('subject')
    teachar_num = request.form.get('teachar_num')
    icon = request.files['icon']
    grade_name = request.form.get('grade_name')
    course = Course(subject=subject)
    course.search_grade(grade_name)
    course.search_teachar(teachar_num)
    db.session.add(course)
    db.session.commit()
    icon.filename = 'course' + str(course.id) + os.path.splitext(icon.filename)[1]
    db.session.commit()
    return jsonify({'event':'true'},search_course(course))



@register_bp.route('/teachar',methods=['POST'])
def teachar():
    password = request.form.get('password')
    avatar = request.files['avatar']
    name =request.form.get('name')
    gender = request.form.get('gender')
    number = request.form.get('number')
    teachar = Teachar(password=password,name=name,gender=gender,number=number)
    db.session.add(teachar)
    db.session.commit()
    avatar.filename = 'teachar' + str(teachar.id) + os.path.splitext(avatar.filename)[1]
    avatar.save(os.path.join(current_app.config['UPLOAD_PATH'],avatar.filename))
    teachar.avatar = avatar.filename
    db.session.commit()
    return jsonify({'event':'true'},search_teachar(teachar))


@register_bp.route('/student',methods=['POST'])
def student():
    password = request.form.get('password')
    avatar = request.files['avatar']
    name = request.form.get('name')
    gender = request.form.get('gender')
    number = request.form.get('number')
    student =Student(number=number,password=password,name=name,gender=gender)
    db.session.add(student)
    db.session.commit()
    avatar.filename = 'student' + str(student.id) + os.path.splitext(avatar.filename)[1]
    avatar.save(os.path.join(current_app.config['UPLOAD_PATH'],avatar.filename))
    student.avatar = avatar.filename
    db.session.commit()
    return jsonify({'event':'true'},search_student(student))


@register_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'],filename)

