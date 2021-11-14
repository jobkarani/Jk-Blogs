from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from ..models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email =StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


