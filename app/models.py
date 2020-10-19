from app import db, migrate, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(id):
    u = User.query.get(id)
    return User(u.firstname, u.lastname, u.username, u.email, u.password)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    
    posts = db.relationship('Post', 
                            backref='author', 
                            primaryjoin="User.id==Post.author_id")
    comments = db.relationship('Comments', 
                            backref='author', 
                            primaryjoin="User.id==Comments.author_id")
    
    """
    followed = db.relationship('Follow', 
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'), 
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    """
        
    def __init__(self, firstname='', lastname='', username='', email='', 
                 password=''): 
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"User('ID: {self.id}, Firstname: {self.firstname}, Lastname: {self.lastname}, Username: {self.username}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_address = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    comments = db.relationship('Comments', backref='post', lazy=True)
    
    def __repr__(self):
        return f"Post('Author ID: {self.author_id}, Title: {self.title}, Date: {self.date}, Text: {self.text}')"


class Comments(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
        
    def __repr__(self):
        return f"Comments('Post ID: {self.post_id}, Author ID: {self.author_id}, Date: {self.date}, Text: {self.text}')"

"""
class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    #timestamp = db.Column(db.DateTime, default=datetime.utcnow)
"""

db.create_all()
