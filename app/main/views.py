from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user,login_user,logout_user

from app.models import User, BlogPost
from .. import db
from .forms import UpdateUserForm,LoginForm,RegistrationForm
from .picture_handler import add_profile_pic

# @main.route('/')
# def index():
#     posts = Post.query.order_by(Post.date_posted.desc()).all()
#     print(posts)
#     return render_template('index.html', posts=posts)

#register
@main


#login

#logout
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))
    # return redirect(url_for("core.index"))


    