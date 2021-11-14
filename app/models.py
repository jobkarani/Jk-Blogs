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
    profile_pic_path = db.Column(db.String(200), nullable=False)
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
