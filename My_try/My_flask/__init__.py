from flask import Flask
from My_flask.extensions import  db,moment,bootstrap,login_manager,Avatars,Dropzone
from My_flask.blueprints.admin import admin_bp
from My_flask.blueprints.auth import auth_bp
from My_flask.blueprints.blog import blog_bp
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('My_flask')
    app.config['WTF_I18N_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                      'sqlite:///' + os.path.join(app.root_path, 'data.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secret string'
    app.config['ALBUMY_UPLOAD_PATH'] = os.path.join(app.root_path,'uploads')
    app.config['UPLOAD_PATH'] = os.path.join(os.path.join(app.root_path,'uploads'), 'videos')
    app.config['AVATARS_SAVE_PATH'] = os.path.join(os.path.join(app.root_path,'uploads'),'avatars')
    app.config['DROPZONE_MAX_FILE_SIZE'] = 50
    app.config['DROPZONE_MAX_FILES'] = 1
    app.config['DROPZONE_DEFAULT_MESSAGE'] = '点击这里，上传文件，但是现在暂不支持此功能'
    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    Avatars.init_app(app)
    Dropzone.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

