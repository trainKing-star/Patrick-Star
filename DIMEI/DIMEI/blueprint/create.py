from flask import Blueprint,request,jsonify,g
from DIMEI.extensions import *
from DIMEI.models import *
import os


create_bp = Blueprint('create',__name__)

@create_bp.route('/homework',methods=['POST'])
@auth_t.login_required
def homework():
    title = request.form.get('title')
    deadline = request.form.get('deadline')
    questionText = request.form.get('questionText')
    questionImages = request.files.getlist('questionImages')
    solutionText = request.form.get('solutionText')
    solutionImages = request.files.getlist('solutionImages')
    course_id = request.form.get('course_id')
    homework = Homework(author_id=g.teachar.id,title=title,deadline=deadline,questionText=questionText,solutionText=solutionText,course_id=course_id)
    db.session.add(homework)
    db.session.commit()
    if questionImages:
        if questionImages[0].filename != '':
            i = 0
            for file in questionImages:
                i = i + 1
                file.filename = 'question' + str(homework.id) + '_' + str(i) + os.path.splitext(file.filename)[1]
                questionImage = QuestionImage(photo=file.filename, homework_id=homework.id)
                file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                db.session.add(questionImage)
                db.session.commit()
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

@create_bp.route('/reply',methods=['POST'])
@auth_s.login_required
def reply():
    replyText = request.form.get('replyText')
    replyImages = request.files.getlist('replyImages')
    homework_id = request.form.get('homework_id')
    if homework_id is not None:
        if Homework.query.get(homework_id) is None:
            return jsonify({'event':'failure'})
        reply = Reply(Text=replyText, homework_id=homework_id, student_id=g.student.id)
        db.session.add(reply)
        db.session.commit()
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
        return jsonify({'event': 'true'}, search_reply(reply))
    return jsonify({'event':'failure'})

@create_bp.route('/discussion_t',methods=['POST'])
@auth_t.login_required
def discussion_t():
    course_id = request.form.get('course_id')
    text = request.form.get('text')
    images = request.files.getlist('images')
    discussion = Discussion(course_id=course_id,teachar_id=g.teachar.id,text=text)
    db.session.add(discussion)
    db.session.commit()
    if images:
        if images[0].filename != '':
            i = 0
            for file in images:
                i = i + 1
                file.filename = 'discussion_t' + str(discussion.id) + '_' + str(g.teachar.id) + '_' + str(i) + \
                                os.path.splitext(file.filename)[1]
                image = DiscussionImage(photo=file.filename, discussion_id=discussion.id)
                file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                db.session.add(image)
                db.session.commit()
    return jsonify({'event':'true'},search_discussion_t(discussion))

@create_bp.route('/like',methods=['POST'])
@auth.login_required
def like():
    name=g.user.name
    number = g.user.number
    discussion_id = request.form.get('discussion_id')
    like = Like(name=name,number=number,discussion_id=discussion_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'event':'true'})

@create_bp.route('/comment',methods=['POST'])
@auth.login_required
def comment():
    detail = request.form.get('detail')
    discussion_id = request.form.get('discussion_id')
    if Discussion.query.get(discussion_id) is None:
        return jsonify({'event':'failure'})
    comment = Comment(detail=detail,discussion_id=discussion_id,publisher=g.user.name)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'event':'true'},search_comment(comment))



@create_bp.route('/discussion_s',methods=['POST'])
@auth_s.login_required
def discussion_s():
    course_id = request.form.get('course_id')
    text = request.form.get('text')
    images = request.files.getlist('images')
    discussion = Discussion(course_id=course_id,student_id=g.student.id,text=text)
    db.session.add(discussion)
    db.session.commit()
    if images:
        if images[0].filename != '':
            i = 0
            for file in images:
                i = i + 1
                file.filename = 'discussion_s' + str(discussion.id) + '_' + str(g.student.id) + '_' + str(i) + \
                                os.path.splitext(file.filename)[1]
                image = DiscussionImage(photo=file.filename, discussion_id=discussion.id)
                file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
                db.session.add(image)
                db.session.commit()
    return jsonify({'event':'true'},search_discussion_s(discussion))

@create_bp.route('/notification',methods=['POST'])
@auth_t.login_required
def notification():
    text = request.form.get('text')
    course_id = request.form.get('course_id')
    notification = Notification(text=text,course_id=course_id)
    db.session.add(notification)
    db.session.commit()
    return jsonify({'event':'true'},search_notifi(notification))
