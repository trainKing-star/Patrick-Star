from DIMEI.extensions import *
from DIMEI.models import *
from flask import Blueprint,request,jsonify,g
import os

update_bp = Blueprint('update',__name__)


@update_bp.route('/course/<int:course_id>',methods=['GET','POST'])
@auth_t.login_required
def update_course(course_id):
    course = Course.query.get(course_id)
    icon = request.files.get('icon')
    if icon is not None:
        icon.filename = 'course' + str(course.id) + os.path.splitext(icon.filename)[1]
        course.icon = icon.filename
        icon.save(os.path.join(current_app.config['UPLOAD_PATH'], icon.filename))
    subject = request.form.get('subject')
    if subject is not None:
        course.subject=subject
    teachar_num = request.form.get('teachar_num')
    if teachar_num is not None:
        teachar = Teachar.query.filter_by(number=teachar_num).first()
        course.teachar_id=teachar.id
    db.session.commit()
    return jsonify({'event':'success'},search_course(course))

@update_bp.route('/teachar',methods=['POST'])
@auth_t.login_required
def update_teachar():
    avatar = request.files.get('avatar')
    if avatar is not None:
        avatar.filename = 'teachar' + str(g.teachar.id) + os.path.splitext(avatar.filename)[1]
        avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
        g.teachar.avatar = avatar.filename
    password = request.form.get('password')
    if password is not None:
        g.teachar.password = password
    db.session.commit()
    return jsonify({'event':'success'},search_teachar(g.teachar))

@update_bp.route('/student',methods=['POST'])
@auth_s.login_required
def update_student():
    avatar = request.files.get('avatar')
    if avatar is not None:
        avatar.filename = 'student' + str(g.student.id) + os.path.splitext(avatar.filename)[1]
        avatar.save(os.path.join(current_app.config['UPLOAD_PATH'], avatar.filename))
        g.student.avatar = avatar.filename
    password = request.form.get('password')
    if password is not None:
        g.student.password = password
    db.session.commit()
    return jsonify({'event':'success'},search_student(g.student))

@update_bp.route('/homework/<int:homework_id>',methods=['POST'])
@auth_t.login_required
def homework(homework_id):
    homework = Homework.query.get(homework_id)
    title = request.form.get('title')
    if title is not None:
        homework.title = title
    deadline = request.form.get('deadline')
    if deadline is not None:
        homework.deadline = deadline
    questionText = request.form.get('questionText')
    if questionText is not None:
        homework.questionText = questionText
    questionImages = request.files.getlist('questionImages')
    solutionText = request.form.get('solutionText')
    if solutionText is not None:
        homework.solutionText = solutionText
    solutionImages = request.files.getlist('solutionImages')
    if questionImages:
        if questionImages[0].filename != '':
            i = 0
            for file in questionImages:
                i = i + 1
                file.filename = 'question' + str(homework.id) + '_' + str(i) + os.path.splitext(file.filename)[1]
                questionImage = QuestionImage(photo=file.filename, homework_id=homework.id)
                file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                db.session.add(questionImage)
    if solutionImages:
        if solutionImages[0].filename != '':
            j = 0
            for file in solutionImages:
                j = j + 1
                file.filename = 'solution' + str(homework.id) + '_' + str(j) + os.path.splitext(file.filename)[1]
                solutionImage = SolutionImage(photo=file.filename, homework_id=homework.id)
                file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                db.session.add(solutionImage)
    db.session.commit()
    return jsonify({'event':'true'},search_homework(homework))

@update_bp.route('/reply_s/<int:reply_id>',methods=['POST'])
@auth_s.login_required
def update_reply_s(reply_id):
    reply = Reply.query.get(reply_id)
    if reply is None:
        return jsonify({'event':'failure'})
    replyText = request.form.get('replyText')
    if replyText is not None:
        reply.Text = replyText
    replyImages = request.files.getlist('replyImages')
    if replyImages is not None:
        if replyImages:
            if replyImages[0].filename != '':
                i = 0
                for file in replyImages:
                    i = i + 1
                    file.filename = 'reply' + '_' + str(reply.id) + '_' + str(g.student.id) + '_' + str(i) + \
                                    os.path.splitext(file.filename)[1]
                    replyImage = ReplyImage(photo=file.filename, reply_id=reply.id)
                    file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                    db.session.add(replyImage)
    db.session.commit()
    return jsonify({'event':'success'},search_reply(reply))

@update_bp.route('/reply_t/<int:reply_id>',methods=['POST'])
@auth_t.login_required
def update_reply_t(reply_id):
    reply = Reply.query.get(reply_id)
    if reply is None:
        return jsonify({'event':'failure'})
    evaluationText = request.form.get('evaluationText')
    if evaluationText is not None:
        reply.evaluationText = evaluationText
    evaluationImages = request.files.getlist('evaluationImages')
    reply.corrected = True
    if evaluationImages is not None:
        if evaluationImages:
            if evaluationImages[0].filename != '':
                i = 0
                for file in evaluationImages:
                    i = i + 1
                    file.filename = 'evaluation' + '_' + str(reply.id) + '_' + str(g.teachar.id) + '_' + str(i) + \
                                    os.path.splitext(file.filename)[1]
                    evaluationImages = EvaluationImage(photo=file.filename, reply_id=reply.id)
                    file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                    db.session.add(evaluationImages)
    db.session.commit()
    return jsonify({'event':'success'},search_reply(reply))
