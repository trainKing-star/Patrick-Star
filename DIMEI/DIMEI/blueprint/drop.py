from flask import Blueprint,jsonify,g
from DIMEI.extensions import *
from DIMEI.models import *


drop_bp = Blueprint('drop',__name__)

@drop_bp.route('/discussion_t/<int:discussion_id>',methods=['DELETE'])
@auth_t.login_required
def delete_d_t(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    if discussion is not None:
        db.session.delete(discussion)
        db.session.commit()
        return jsonify({'event':'success'})
    return jsonify({'event':'failure'})

@drop_bp.route('/discussion_s/<int:discussion_id>',methods=['DELETE'])
@auth.login_required
def delete_d_s(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    if discussion is not None:
        db.session.delete(discussion)
        db.session.commit()
        return jsonify({'event':'success'})
    return jsonify({'event':'failure'})

@drop_bp.route('/notification/<int:no_id>',methods=['DELETE'])
@auth_t.login_required
def delete_n(no_id):
    notification = Notification.query.get(no_id)
    if notification is not None:
        db.session.delete(notification)
        db.session.commit()
        return jsonify({'event':'success'})
    return jsonify({'event':'failure'})

@drop_bp.route('/comment/<int:comment_id>',methods=['DELETE'])
@auth_t.login_required
def delete_c(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is not None:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'event':'success'})
    return jsonify({'event':'failure'})

@drop_bp.route('/homework/<int:homework_id>',methods=['DELETE'])
@auth_t.login_required
def delete_h(homework_id):
    homework = Homework.query.get(homework_id)
    if homework is not None:
        db.session.delete(homework)
        db.session.commit()
        return jsonify({'event':'success'})
    return jsonify({'event':'failure'})

@drop_bp.route('/like/<int:like_id>',methods=['DELETE'])
@auth.login_required
def delete_ll(like_id):
    like = Like.query.get(like_id)
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'event':'success'})
    return jsonify({'event':'failure'})