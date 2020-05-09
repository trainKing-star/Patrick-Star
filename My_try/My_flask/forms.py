from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField ,SubmitField ,BooleanField,SelectField,ValidationError,TextAreaField,FileField
from wtforms.validators import  DataRequired,Length
from My_flask.models import  Category

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 8)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 10)])
    remember = BooleanField('记住我',default=False)
    submit = SubmitField('提交')

class DeleteForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 8)])
    submit = SubmitField('提交')

class Update_dataForm(FlaskForm):
    password1 = PasswordField('修改密码', validators=[DataRequired(), Length(1, 10)])
    password2 = PasswordField('确定密码', validators=[DataRequired(), Length(1, 10)])
    recomment = TextAreaField('个性说说',validators=[DataRequired()])
    submit = SubmitField('提交')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 8)])
    password1 = PasswordField('密码', validators=[DataRequired(), Length(1, 10)])
    password2 = PasswordField('确定密码', validators=[DataRequired(), Length(1, 10)])
    submit = SubmitField('注册')

class VideoForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int)
    video = FileField('视频上传',validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('分类名', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('提交')

class CategoryForm1(FlaskForm):
    name = StringField('分类名', validators=[DataRequired(), Length(1, 30)])
    submit1 = SubmitField('提交')

class CommentForm(FlaskForm):
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('提交')

class PhotoForm(FlaskForm):
    photo = FileField('图片上传',validators=[DataRequired()])
    submit = SubmitField('提交')

class VideodeleteForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(VideodeleteForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]

