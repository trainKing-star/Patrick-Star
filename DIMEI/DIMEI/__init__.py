from flask import Flask
from DIMEI.settings import config
from DIMEI.extensions import db,faker
from DIMEI.models import *
from DIMEI.blueprint.login import login_bp
from DIMEI.blueprint.create import create_bp
from DIMEI.blueprint.drop import drop_bp
from DIMEI.blueprint.show import show_bp
from DIMEI.blueprint.register import register_bp
import os
import click


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('DIMEI')
    app.config.from_object(config[config_name])
    app.config['UPLOAD_PATH'] = os.path.join(os.path.join(app.root_path,'uploads'),'avatars')

    register_extensions(app)
    register_blueprints(app)
    register_error(app)
    register_command(app)

    return app

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app):
    app.register_blueprint(create_bp,url_prefix='/create')
    app.register_blueprint(drop_bp,url_prefix='/drop')
    app.register_blueprint(login_bp,url_prefix='/login')
    app.register_blueprint(register_bp,url_prefix='/register')
    app.register_blueprint(show_bp,url_prefix='/show')

def register_error(app):
    pass

def register_command(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        click.echo('create success')


    @app.cli.command()
    @click.option('--num',default=10)
    def create(num):
        while num:
            num=num-1
            school = School(name=faker.province()+faker.city_suffix()+'一中')
            db.session.add(school)
            db.session.commit()
            click.echo('OK')
            for i in range(10):
                grade = Grade(name='高一'+'('+str(i)+')班',school_id=school.id)
                db.session.add(grade)
                db.session.commit()
                for j in range(4):
                    teachar = Teachar(name=faker.name(),number=faker.phone_number(),password=faker.phone_number())
                    db.session.add(teachar)
                    db.session.commit()
                    subject=['语文','数学','英语','科学']
                    course = Course(subject=subject[j],teachar_id=teachar.id,grade_id=grade.id)
                    db.session.add(course)
                    db.session.commit()
                for k in range(10):
                    student = Student(number=faker.phone_number(),password=faker.phone_number(),name=faker.name(),grade_id=grade.id)
                    db.session.add(student)
                    db.session.commit()
        click.echo('create success')

