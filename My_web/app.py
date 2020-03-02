from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,fields,marshal_with,reqparse,Api
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL','sqlite:///'+os.path.join(app.root_path,'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
api = Api(app)
'''
    你需要先post提供一个数据，才能进行其他操作，因为post中会创造一个数据库表单
'''
class User(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    content = db.Column(db.Text)
    state = db.Column(db.String ,default= False)
    strat_time = db.Column(db.String)
    end_time = db.Column(db.String)

resource_fields = {
    'id': fields.Integer,
    'content': fields.String ,
    'state': fields.String ,
    'strat_time': fields.String ,
    'end_time': fields.String ,
}

get_parser = reqparse.RequestParser()
get_parser.add_argument(
    'id', type=int, help=('请输入正确的ID'),
)

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'content',type=str,help=('请输入正确的内容'),
)
post_parser.add_argument(
    'state',type=str,help=('请输入正确的状态'),
)
post_parser.add_argument(
    'strat_time',type=str,help=('请输入正确的时间'),
)
post_parser.add_argument(
    'end_time',type=str,help=('请输入正确的时间'),
)

class User_data(Resource):

    @marshal_with(resource_fields)
    def get(self,id):
        args = get_parser.parse_args()
        user = User.query.get(id)
        return user

class User_post(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = post_parser.parse_args()
        user = User(content=args.content,state=args.state,strat_time=args.strat_time,end_time=args.end_time)
        db.create_all()
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self,id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return 'delete success'

    @marshal_with(resource_fields)
    def put(self,id):
        args = post_parser.parse_args()
        user =User.query.get(id)
        user.state=args.state
        db.session.commit()
        return user

class User_post1(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = post_parser.parse_args()
        users = User.query.filter(User.state==args.state).all()
        return users

    def delete(self):
        args = post_parser.parse_args()
        users = User.query.filter(User.state==args.state).all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return 'delete success'

    def put(self):
        args = post_parser.parse_args()
        users = User.query.filter(User.state!=args.state).all()
        for user in users:
            user.state = args.state
        db.session.commit()
        return 'update successs'

class User_post2(Resource):
    @marshal_with(resource_fields)
    def get(self):
        if User.query.all():
            users = User.query.all()
            return users
        else:
            return 'no information'

    def delete(self):
        db.drop_all()
        return 'delete success'



'''根据索引，使用get方法返回一个事项'''
api.add_resource(User_data,'/<int:id>')

'''post:创建一个事项并存入数据库  delete_one：根据索引,从数据库中删除一个事项  put_one：根据索引，更新一个事项并同步到数据库'''
api.add_resource(User_post,'/post','/delete_one/<int:id>','/put_one/<int:id>')

'''get_select:指定访问待办或者已完成的所有事项  delete_select:指定删除待办或者已完成的所有事项  put_selsect:修改指定的所有待办或者已完成事项'''
api.add_resource(User_post1,'/get_select','/delete_select','/put_select')

'''get_all:访问所有事项  delete_all:删除所有事项'''
api.add_resource(User_post2,'/get_all','/delete_all')

if __name__ == '__main__':
    app.run()

