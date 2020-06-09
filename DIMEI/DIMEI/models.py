from DIMEI.extensions import db
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature
from passlib.apps import custom_app_context as pwd_context

association_table_grade = db.Table('association',db.Column('grade_id',db.Integer,db.ForeignKey('grade.id')),db.Column('teachar_id',db.Integer,db.ForeignKey('teachar.id')))

class Teachar(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    number = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    gender = db.Column(db.String)
    #grades = db.relationship('Grade',secondary=association_table_grade,back_populates='teachars')
    courses = db.relationship('Course',back_populates='teachar',cascade='all')
    discussions = db.relationship('Discussion',back_populates='teachar',cascade='all')
    homeworks = db.relationship('Homework',back_populates='author',cascade='all')

    def generate_auth_token(self,expiration=6000):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'teachar_id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        try:
            id=data['teachar_id']
        except KeyError:
            return None
        teachar = Teachar.query.get(id)
        return teachar


class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    number = db.Column(db.String)
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.id'))
    grade = db.relationship('Grade',back_populates='students')
    replies = db.relationship('Reply',back_populates='student',cascade='all')
    discussions = db.relationship('Discussion',back_populates='student',cascade='all')

    def generate_auth_token(self,expiration=6000):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'student_id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        try:
            id=data['student_id']
        except KeyError:
            return None
        student = Student.query.get(id)
        return student

    def sreach_grade(self,name):
        grade = Grade.query.filter_by(name=name).first()
        self.grade_id = grade.id


class School(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    hash_name = db.Column(db.String)
    grades = db.relationship('Grade',back_populates='school',cascade='all')

    def hashname(self):
        self.hash_name=pwd_context.encrypt(self.name)

class Grade(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship('School',back_populates='grades')
    #teachars = db.relationship('Teachar', secondary=association_table_grade,back_populates='grades')
    students = db.relationship('Student', back_populates='grade', cascade='all')
    courses = db.relationship('Course',back_populates='grade',cascade='all')

    def search_school(self,name):
        school = School.query.filter_by(name=name).first()
        self.school_id = school.id


class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String)
    teachar_id = db.Column(db.Integer,db.ForeignKey('teachar.id'))
    teachar = db.relationship('Teachar',back_populates='courses')
    grade = db.relationship('Grade',back_populates='courses')
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.id'))
    icon = db.Column(db.String)
    homeworks = db.relationship('Homework',back_populates='course',cascade='all')
    discussions = db.relationship('Discussion',back_populates='course')
    notifications = db.relationship('Notification',back_populates='course',cascade='all')

    def search_teachar(self,number):
        teachar = Teachar.query.filter_by(number=number).first()
        self.teachar_id = teachar.id



class Notification(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    course = db.relationship('Course',back_populates='notifications')


class Discussion(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    teachar_id = db.Column(db.Integer,db.ForeignKey('teachar.id'))
    teachar = db.relationship('Teachar',back_populates='discussions')
    student_id =db.Column(db.Integer,db.ForeignKey('student.id'))
    student = db.relationship('Student',back_populates='discussions')
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    course = db.relationship('Course',back_populates='discussions')
    text = db.Column(db.Text)
    images=db.relationship('DiscussionImage',back_populates='discussion',cascade='all')
    time = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    likes = db.relationship('Like',back_populates='discussion',cascade='all')
    comments = db.relationship('Comment',back_populates='discussion',cascade='all')

class Like(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    discussion = db.relationship('Discussion',back_populates='likes')
    discussion_id = db.Column(db.Integer,db.ForeignKey('discussion.id'))

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    detail = db.Column(db.Text)
    publisher = db.Column(db.String)
    discussion_id = db.Column(db.Integer,db.ForeignKey('discussion.id'))
    discussion = db.relationship('Discussion',back_populates='comments')

class DiscussionImage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    photo = db.Column(db.String)
    discussion_id = db.Column(db.Integer,db.ForeignKey('discussion.id'))
    discussion = db.relationship('Discussion',back_populates='images')


class Homework(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    course = db.relationship('Course',back_populates='homeworks')
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('teachar.id'))
    author=db.relationship('Teachar',back_populates='homeworks')
    title = db.Column(db.String)
    releaseTime = db.Column(db.String,default=datetime.utcnow,index=True)
    deadline = db.Column(db.String)
    questionText = db.Column(db.Text)
    questionImages = db.relationship('QuestionImage',back_populates='homework',cascade='all')
    replies = db.relationship('Reply',back_populates='homework',cascade='all')
    solutionText = db.Column(db.Text)
    solutionImages = db.relationship('SolutionImage',back_populates='homework',cascade='all')


class QuestionImage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    photo = db.Column(db.String)
    homework = db.relationship('Homework',back_populates='questionImages')
    homework_id = db.Column(db.Integer,db.ForeignKey('homework.id'))

class SolutionImage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    photo = db.Column(db.String)
    homework = db.relationship('Homework',back_populates='solutionImages')
    homework_id = db.Column(db.Integer,db.ForeignKey('homework.id'))

class Reply(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Text=db.Column(db.Text)
    finished = db.Column(db.Boolean, default=False)
    corrected = db.Column(db.Boolean, default=False)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    student = db.relationship('Student',back_populates='replies')
    homework = db.relationship('Homework',back_populates='replies')
    homework_id = db.Column(db.Integer,db.ForeignKey('homework.id'))
    replyImages = db.relationship('ReplyImage',back_populates='reply',cascade='all')
    evaluationText = db.Column(db.Text)
    evaluationImages = db.relationship('EvaluationImage',back_populates='reply',cascade='all')

class EvaluationImage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    photo = db.Column(db.String)
    reply = db.relationship('Reply',back_populates='evaluationImages')
    reply_id = db.Column(db.Integer,db.ForeignKey('reply.id'))

class ReplyImage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    photo = db.Column(db.String)
    reply_id = db.Column(db.Integer,db.ForeignKey('reply.id'))
    reply = db.relationship('Reply',back_populates='replyImages')