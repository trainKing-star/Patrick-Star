from flask import Blueprint,g,jsonify
from DIMEI.models import Teachar,Student
from DIMEI.extensions import auth_t,auth_s,auth


login_bp = Blueprint('login',__name__)

@login_bp.route('/teachar')
@auth_t.login_required
def get_auth_token_t():
    token = g.teachar.generate_auth_token()
    return jsonify({'token':token.decode('ascii')})

@auth_t.verify_password
def verify_password_t(number_or_token,password):
    teachar = Teachar.verify_auth_token(number_or_token)
    if not teachar:
        teachar = Teachar.query.filter_by(number=number_or_token).first()
        if not teachar or not teachar.password==password:
            return False
        g.teachar = teachar
        return True
    g.teachar = teachar
    return True

@login_bp.route('/student')
@auth_s.login_required
def get_auth_token_s():
    token = g.student.generate_auth_token()
    return jsonify({'token':token.decode('ascii')})

@auth_s.verify_password
def verify_password_s(number_or_token,password):
    student = Student.verify_auth_token(number_or_token)
    if not student:
        student = Student.query.filter_by(number=number_or_token).first()
        if not student or not student.password==password:
            return False
        g.student = student
        return True
    g.student = student
    return True

@auth.verify_password
def verify_password(token,password):
    teachar = Teachar.verify_auth_token(token)
    if not teachar:
        student = Student.verify_auth_token(token)
        if not student:
            return False
        g.user=student
        return True
    g.user=teachar
    return True
