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

@main.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blogposts.html',blog_posts=blog_posts,user=user)


@main.route('/comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name=form.name.data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully.')
        return redirect(url_for('.index'))
    return render_template('comments.html', form=form)

@main.route('/comment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    """
        View delete comment function that returns the delete comment page and its data
    """
    comment = Comment.get_comment(id)
    # if comment.user_id != current_user:
    #     abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('You have successfully deleted the comment', 'success')
    return redirect(url_for('main.account', username=current_user.username))
    