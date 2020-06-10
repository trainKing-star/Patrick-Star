from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from faker import Faker

db = SQLAlchemy()
auth_t = HTTPBasicAuth()
auth_s = HTTPBasicAuth()
auth = HTTPBasicAuth()
faker = Faker('zh_CN')



def search_teachar(teachar):
    return {
        'id':teachar.id,
        'number':teachar.number,
        'password':teachar.password,
        'avatar':teachar.avatar,
        'name':teachar.name,
        'gender':teachar.gender,
        #'grades':[search_grade_teachar(grade) for grade in teachar.grades],
        'courses':[search_course_teachar(course) for course in teachar.courses],
        'discussions':[search_discussion_teachar(discussion) for discussion in teachar.discussions]
    }

def search_grade_teachar(grade):
    return {
        'grade_id':grade.id,
        'grade':grade.name,
    }

def search_grade(grade):
    return {
        'grade_id':grade.id,
        'grade':grade.name,
        'courses':[search_course_grade(course) for course in grade.courses],
        'students':[search_student(student) for student in grade.students]
    }


def search_grade_school(grade):
    return {
        'grade_id':grade.id,
        'grade':grade.name
    }

def search_course_grade(course):
    return {
        'course_id':course.id,
        'subject':course.subject,
        'teachar':course.teachar.name
    }

def search_course_teachar(course):
    return {
        'course_id':course.id,
        'subject':course.subject,
        'grade':course.grade.name,
        'school':course.grade.school.name
    }

def search_discussion_teachar(discussion):
    return {
        'discussion_id':discussion.id,
        'text':discussion.text
    }

def search_student(student):
    return {
        'id':student.id,
        'number':student.number,
        'password':student.password,
        'avatar':student.avatar,
        'gender':student.gender,
        'name':student.name,
        'grade_id':student.grade.id,
        'discussions':[search_discussion_teachar(discussion) for discussion in student.discussions]
    }

def search_course(course):
    return {
        'course_id':course.id,
        'grade_id':course.grade.id,
        'subject':course.subject,
        'teachar':course.teachar.name,
        'icon':course.icon,
        'homeworks':[search_homework_course(homework) for homework in course.homeworks],
        'discussions':[search_discussion_teachar(discussion) for discussion in course.discussions],
        'notifications':[search_notification(notification) for notification in course.notifications]
    }


def search_notification(notification):
    return {
        'notification_id':notification.id,
        'text':notification.text,
        'time':notification.time
    }

def search_homework_course(homework):
    return {
        'homework_id':homework.id,
        'author':homework.author.name,
        'title':homework.title,
        'author_id':homework.author.id
    }

def search_discussion_t(discussion):
    return {
        'discussion_id':discussion.id,
        'author_id':discussion.teachar.number,
        'publisher':discussion.teachar.name,
        'avatar':discussion.teachar.avatar,
        'text':discussion.text,
        'images':[search_images(discussionImage) for discussionImage in discussion.images],
        'time':discussion.time,
        'count': len(discussion.likes),
        'likes': [search_like(like) for like in discussion.likes],
        'comments':[search_comment(comment) for comment in discussion.comments]
    }

def search_discussion_s(discussion):
    return {
        'discussion_id':discussion.id,
        'author_id':discussion.student.number,
        'publisher':discussion.student.name,
        'avatar':discussion.student.avatar,
        'text':discussion.text,
        'images':[search_images(discussionImage) for discussionImage in discussion.images],
        'time':discussion.time,
        'count': len(discussion.likes),
        'likes':[search_like(like) for like in discussion.likes],
        'comments':[search_comment(comment) for comment in discussion.comments]
    }

def search_like(like):
    return {
        'like_id':like.id,
        'number':like.number,
        'name':like.name
    }


def search_images(discussionImage):
    return {
        'image_id':discussionImage.id,
        'image':discussionImage.photo
    }

def search_comment(comment):
    return {
        'comment_id':comment.id,
        'publisher':comment.publisher,
        'detail':comment.detail
    }


def search_homework(homework):
    return {
        'homework_id':homework.id,
        'title':homework.title,
        'author':homework.author.name,
        'releaseTime':homework.releaseTime,
        'deadline':homework.deadline,
        'questionText':homework.questionText,
        'questionImages':[{'questionImage':questionImage.photo} for questionImage in homework.questionImages],
        'solutionText':homework.solutionText,
        'solutionImages':[{'solutionImage':solutionImage.photo} for solutionImage in homework.solutionImages] ,
        'reply':[search_reply(reply) for reply in homework.replies],
        'author_num':homework.author.number,
        'course_id':homework.course.id
    }


def search_reply(reply):
    return {
        'reply_id':reply.id,
        'student':reply.student.name,
        'homework_id':reply.homework.id,
        'student_num':reply.student.number,
        'replyText':reply.Text,
        'corrected':reply.corrected,
        'finished':reply.finished,
        'replyImages':[{'replyImage':replyImage.photo} for replyImage in reply.replyImages],
        'evaluationText': reply.evaluationText,
        'evaluationImages': [{'evaluationImage': evaluationImage.photo} for evaluationImage in reply.evaluationImages]
    }


def search_school(school):
    return {
        'school_id':school.id,
        'name':school.name,
        'grades':[search_grade_school(grade) for grade in school.grades],
        'hashname':school.hash_name
    }


def search_notifi(notification):
    return {
        'text':notification.text,
        'time':notification.time,
        'course_id':notification.course.id
    }