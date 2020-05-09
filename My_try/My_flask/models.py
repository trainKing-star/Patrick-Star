from My_flask.extensions import  db
from datetime import datetime
from flask_login import UserMixin
from flask_avatars import Identicon


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    recomment = db.Column(db.Text,default='这个人很懒，没什么留下')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    video = db.relationship('Video',back_populates='admin',cascade='all,delete-orphan')
    comment = db.relationship('Comment', back_populates='admin', cascade='all,delete-orphan')
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))

    def __init__(self,**kwargs):
        super(Admin,self).__init__(**kwargs)
        self.generate_avatar()

    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(8),unique=True)
    videos = db.relationship('Video', back_populates='category')

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    videoname = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    admin = db.relationship('Admin',back_populates='video')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='videos')
    comments = db.relationship('Comment', back_populates='video', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    reviewed = db.Column(db.Boolean,default=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    video_id = db.Column(db.Integer,db.ForeignKey('video.id'))
    video = db.relationship('Video',back_populates='comments')
    replied_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
    replied = db.relationship('Comment',back_populates='replies',remote_side=[id])
    replies = db.relationship('Comment',back_populates='replied',cascade='all')
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    admin = db.relationship('Admin', back_populates='comment')





