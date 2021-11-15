from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager



class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),unique=True,index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    hashed_pass = db.Column(db.String(255))
    profile_pic = db.Column(db.String(200), nullable=False, default='default_profile.png')
    posts = db.relationship('BlogPost', backref='author', lazy='dynamic')

    def __init__(self,email,username,password):
        self.email =email
        self.username = username
        self.hashed_pass =generate_password_hash(password)


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.hashed_pass = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_pass, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    def __repr__(self):
        return f'Username {self.username}'


class BlogPost(db.Model):

    __tablename__ = 'blogs'
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    date =db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(255),nullable=False)
    text = db.Column(db.String,nullable=False)


    def __init__(self,title,text,user_id):
        self.title = title
        self.text =text
        self.user_id =user_id


    def __repr__(self):
        return f"Post ID: {self.id} --Title: {self.date} --Date: {self.date}"


class Comment(db.Model):
    tablename = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))
    

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return comments

    @classmethod
    def get_comment_author(cls, user_id):
        author = User.query.filter_by(id=user_id).first()

        return author

    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()