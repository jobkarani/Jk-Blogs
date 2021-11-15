from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user,login_user,logout_user

from app.models import User, BlogPost
from .. import db
from .forms import UpdateUserForm,LoginForm,RegistrationForm
from .picture_handler import add_profile_pic

@main.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.id).all()
    print(posts)
    return render_template('index.html', posts=posts)

    
#register
@main.route('/register',methods = ['GET','POST'])
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
@main.route('/login',methods=['Get','POST'])
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

return render_template('login.html',form=form, email=email, password=password)



#logout
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))
    # return redirect(url_for("core.index"))

#account
@main.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_pic = pic

        current_user.username =form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User account Succefully Updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_pic = url_for('static',filename='profile_pics/'+current_user.profile_pic)
    return render_template('account.html',profile_pic=profile_pic,form=form)





    