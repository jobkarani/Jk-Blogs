from flask import render_template, redirect, url_for, abort, flash, request
from . import auth
from flask_login import login_required, current_user,login_user,logout_user

from ..models import User, BlogPost
from .. import db
from .forms import UpdateUserForm,LoginForm,RegistrationForm
from .picture_handler import add_profile_pic

#register
@auth.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!!')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form, email=email, username=username, password=password)



#login
@auth.route('/login',methods=['Get','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

    user = User.query.filter_by(email=form.email.data).first()

    if user.check_password_hash(form.password.data) and user is not None:

        login_user(user)
        flash('Log in was Successful!')
        
        next = request.args.get('next')

        if next ==None or not next[0] == '/':
            next = url_for('index')
            # next = url_for('core.index')

        return redirect(next)

    return render_template('login.html',form=form)



#logout
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))
    # return redirect(url_for("core.index"))


    