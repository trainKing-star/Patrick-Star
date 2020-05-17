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
        'courses':[search_course_grade(course) for course in grade.courses]
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
        #'courses':[search_course_teachar(course) for course in student.grade.courses],
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
        'notifications':[search_notification(notification) for notification in course.notifications]
    }

def search_notification(notification):
    return {
        'notification_id':notification.id,
        'text':notification.text
    }

def search_homework_course(homework):
    return {
        'homework_id':homework.id,
        'author':homework.author,
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
        'likes':
            {
                'count':len(discussion.likes),
                'name':[like.name for like in discussion.likes]
            },
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
        'likes':
            {
                'count':len(discussion.likes),
                'name':[like.name for like in discussion.likes]
            },
        'comments':[search_comment(comment) for comment in discussion.comments]
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
        'releaseTime':homework.releaseTime,
        'deadline':homework.deadline,
        'questionText':homework.questionText,
        'questionImages':[{'questionImage':questionImage.photo} for questionImage in homework.questionImages],
        'solutionText':homework.solutionText,
        'solutionImages':[{'solutionImage':solutionImage.photo} for solutionImage in homework.solutionImages] ,
        'finished':homework.finished,
        'corrected':homework.corrected,
        'reply':[search_reply(reply) for reply in homework.replies],
        'author_num':homework.author.number,
        'course_id':homework.course.id
    }

def search_reply(reply):
    return {
        'homework_id':reply.homework.id,
        'author_id':reply.student.id,
        'replyText':reply.Text,
        'replyImages':[{'replyImage':replyImage.photo} for replyImage in reply.replyImages]
    }


def search_school(school):
    return {
        'school_id':school.id,
        'name':school.name,
        'grades':[search_grade_school(grade) for grade in school.grades]
    }


def search_notifi(notification):
    return {
        'text':notification.text,
        'course_id':notification.course.id
    }