from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from ..models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email =StringField('Email', validators=[Required(),Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email =StringField('Email', validators=[Required(),Email()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required(),EqualTo('confirm_pass',message='Passwords must match!')])
    confirm_pass = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('Register!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email name is already taken!!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken!!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    post = TextAreaField('Blog', validators=[Required()])
    submit = SubmitField('Post Blog')

class UpdateUserForm(FlaskForm):
    email =StringField('Email', validators=[Required(),Email()])
    username = StringField('Username', validators=[Required()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email name is already taken!!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken!!')

class CommentsForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Comment')