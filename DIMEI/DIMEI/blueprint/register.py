from DIMEI.extensions import *
from DIMEI.models import School,Teachar,Student,Grade,Course
from flask import render_template,Blueprint,request,jsonify,url_for,send_from_directory,current_app
import os

register_bp = Blueprint('register',__name__)


@register_bp.route('/school',methods=['POST'])
def school():
    name = request.form.get('name')
    school = School(name=name)
    school.hashname()
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
    icon = request.files.get('icon')
    grade_id = request.form.get('grade_id')
    course = Course(subject=subject,grade_id=grade_id)
    course.search_teachar(teachar_num)
    db.session.add(course)
    db.session.commit()
    if icon is not None:
        icon.filename = 'course' + str(course.id) + os.path.splitext(icon.filename)[1]
        course.icon = icon.filename
        icon.save(os.path.join(current_app.config['UPLOAD_PATH'], icon.filename))
        db.session.commit()
    return jsonify({'event':'true'},search_course(course))



@register_bp.route('/teachar',methods=['POST'])
def teachar():
    password = request.form.get('password')
    avatar = request.files.get('avatar')
    name =request.form.get('name')
    gender = request.form.get('gender')
    number = request.form.get('number')
    teachar = Teachar(password=password,name=name,gender=gender,number=number)
    db.session.add(teachar)
    db.session.commit()
    if avatar is not None:
        avatar.filename = 'teachar' + str(teachar.id) + os.path.splitext(avatar.filename)[1]
        avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
        teachar.avatar = avatar.filename
        db.session.commit()
    return jsonify({'event':'true'},search_teachar(teachar))


@register_bp.route('/student',methods=['POST'])
def student():
    password = request.form.get('password')
    avatar = request.files.get('avatar')
    name = request.form.get('name')
    gender = request.form.get('gender')
    number = request.form.get('number')
    grade = request.form.get('grade_id')
    student =Student(number=number,password=password,name=name,gender=gender,grade_id=grade)
    db.session.add(student)
    db.session.commit()
    if avatar is not None:
        avatar.filename = 'student' + str(student.id) + os.path.splitext(avatar.filename)[1]
        avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
        student.avatar = avatar.filename
        db.session.commit()
    return jsonify({'event':'true'},search_student(student))



