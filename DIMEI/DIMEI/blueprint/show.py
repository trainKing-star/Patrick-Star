from flask import Blueprint,jsonify,request
from DIMEI.models import *
from DIMEI.extensions import *
from flask import send_from_directory,current_app

show_bp = Blueprint('show',__name__)


@show_bp.route('/avatars/<path:filename>',methods=['GET'])
def index(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename,as_attachment=True)

@show_bp.route('/school/all',methods=['GET'])
def school_all():
    schools = School.query.all()
    return jsonify({'schools':[search_school(school) for school in schools]})

@show_bp.route('/school',methods=['GET'])
def school_one():
    schoolname = request.args.get('schoolname')
    school = School.query.filter_by(name=schoolname).first()
    if not school:
        return jsonify({'event':'no school'})
    return jsonify(search_school(school))

@show_bp.route('/teachar/all')
def teachar_all():
    teachars = Teachar.query.all()
    return jsonify({'teachars':[search_teachar(teachar) for teachar in teachars]})


@show_bp.route('/teachar',methods=['GET'])
def teachar_one():
    number = request.args.get('number')
    teachar = Teachar.query.filter_by(number=number).first()
    if not teachar:
        return jsonify({'evnent':'no teachar'})
    return jsonify({'event':'success'},search_teachar(teachar))

@show_bp.route('/student/all')
def student_all():
    students = Student.query.all()
    return jsonify({'students':[search_student(student) for student in students]})

@show_bp.route('/student')
def student_one():
    number = request.args.get('number')
    student = Student.query.filter_by(number=number).first()
    if not student:
        return jsonify({'event':'no student '})
    return jsonify({'event':'success'},search_student(student))

@show_bp.route('/grade/all')
def grade_all():
    grades = Grade.query.all()
    return jsonify({'grades':[search_grade(grade) for grade in grades]})

@show_bp.route('/grade')
def grade_one():
    gradename = request.args.get('gradename')
    grade = Grade.query.filter_by(name=gradename).first()
    if not grade:
        return jsonify({'event':'no grade'})
    return jsonify({'event':'success'},search_grade(grade))

@show_bp.route('/course/<int:course_id>')
def course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'event':'no course'})
    return jsonify({'event':'success'},search_course(course))

@show_bp.route('/homework/<int:homework_id>')
def homework(homework_id):
    homework = Homework.query.get(homework_id)
    if not homework:
        return jsonify({'event':'no homework'})
    return jsonify({'event':'success'},search_homework(homework))

@show_bp.route('/discussion_t/<int:discussion_id>')
def discussion_t(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    if not discussion:
        return jsonify({'event':'no discussion'})
    return jsonify({'event':'success'},search_discussion_t(discussion))

@show_bp.route('/discussion_s/<int:discussion_id>')
def discussion_s(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    if not discussion:
        return jsonify({'event':'no discussion'})
    return jsonify({'event':'success'},search_discussion_t(discussion))