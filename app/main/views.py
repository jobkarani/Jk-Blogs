from flask import render_template, redirect, url_for, abort, flash, request
from requests.api import post
from . import main
from flask_login import login_required, current_user,login_user,logout_user

from app.models import User, BlogPost,Comment,Quote
from .. import db
from ..requests import get_quote
from .forms import UpdateUserForm,LoginForm,RegistrationForm,PostForm,CommentsForm
from .picture_handler import add_profile_pic

@main.route('/')
def index():
    
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=4)
    return render_template('index.html', blog_posts=blog_posts)


#register
@main.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!!')
        return redirect(url_for('main.login'))
    return render_template('main/register.html',form=form)



#login
@main.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index',username=current_user.username))

        flash('Invalid username or Password')

    title = "Jk-Blogs login"
    return render_template('main/login.html',title=title,form=login_form)

#logout
@main.route('/logout')
def logout():
    logout_user()
    # return redirect(url_for("index"))
    return redirect(url_for("main.index"))

#account
@main.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)

        current_user.username =form.username.data
        current_user.email = form.email.data
        current_user.post = form
        db.session.commit()
        flash('User account Succefully Updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_pic = url_for('static',filename='photos/'+current_user.profile_pic)
    return render_template('profile/account.html',profile_pic=profile_pic,form=form)

@main.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=3)
    return render_template('profile/user_blogposts.html',blog_posts=blog_posts,user=user)

@main.route('/addpost',methods = ['GET', 'POST'])
@login_required
def addposts():
    form = PostForm()
    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data, post=form.post.data, user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('main.index'))

    return render_template('addpost.html', form=form)

@main.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    
    return render_template('blog_post.html', title=blog_post.title,date=blog_post,post=blog_post)

@main.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post=BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.post = form.post.data

        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('main.blog_post',blog_post_id=blog_post.id))

    elif request.method  == 'GET':

        form.title.data = blog_post.title
        form.post.data = blog_post.post

    return render_template('addpost.html',title = 'Updating',form=form)

@main.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
    blog_post=BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

        db.session.delete(blog_post)
        db.session.commit()
        flash('Blog post Deleted')
        return redirect(url_for('main.blog_post',blog_post_id=blog_post_id))

    elif request.method  == 'GET':

        form.title.data = blog_post.title
        form.post.data = blog_post.post

    return render_template('index.html',title = 'Deleting',form=form)



@main.route('/comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentsForm()
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

@main.route('/quotes')
def quotes():

    '''
    '''
    quote = get_quote()
    title = 'LetsBlog | Quotes'
    
    return render_template('index.html', title = title,quote = quote)
    