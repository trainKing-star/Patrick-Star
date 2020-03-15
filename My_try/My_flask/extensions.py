from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_avatars import Avatars
from flask_dropzone import Dropzone

db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
bootstrap = Bootstrap()
Avatars = Avatars()
Dropzone = Dropzone()


@login_manager.user_loader
def load_user(user_id):
    from My_flask.models import  Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'blog.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = '请先登录'
