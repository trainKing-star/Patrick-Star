from flask import Flask
from catchat.settings import  config
from catchat.blueprints.admin import  admin_bp
from catchat.blueprints.auth import  auth_bp
from catchat.blueprints.chat import  chat_bp
from catchat.blueprints.oauth import  oauth_bp
from catchat.blueprints.api import api_bp
from catchat.extensions import  db,login_manager,mail,Api,socketio
import click
import os


def create_app(config_name=None):
    if config_name == None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('catchat',static_folder='./dist/static',template_folder='./dist')
    app.config.from_object(config[config_name])
    app.config['AVATARS_SAVE_PATH'] =os.path.join(os.path.join(app.root_path,'dist','static'))
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = '1193299044@qq.com'
    app.config['MAIL_PASSWORD'] = 'aukhycltzpgzffhi'
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('聊天室管理','1193299044@qq.com')
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)
    Api.init_app(app)

def register_blueprints(app):
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(chat_bp)
    app.register_blueprint(oauth_bp,url_prefix='/oauth')
    app.register_blueprint(api_bp,url_prefix='/api')
def register_commands(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        click.echo('create success')


    @app.cli.command()
    @click.option('--count',default=20,help='生成用户数据，默认20条')
    def forge(count):
        from catchat.extensions import  faker
        from catchat.models import  User
        click.echo('Working...')

        for i in range(count):
            user = User(
                username=faker.name(),
                password_hash= faker.phone_number(),
                telephone= faker.phone_number(),
                email_hash= faker.email(),
                country= faker.country()
            )
            db.session.add(user)

        db.session.commit()
        click.echo('Create %d faker user' % count)

