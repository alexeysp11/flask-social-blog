""""
>>> from app.models import db
>>> db.create_all()
>>> from app.models import User, Post, Comments
>>> User.query.all()
[]
>>> user01 = User(firstname='firstname01', lastname='lastname01', username='username01', email='username01@example.com', password='password01')
>>> db.session.add(user01)
>>> db.session.commit()
>>> User.query.all()
[User('1, firstname01, lastname01, username01')]
>>> post01 = Post(post_address='post01', title='Post01', text='Some text for Post01')
>>> user01.posts.append(post01)
>>> db.session.commit()
"""


from app import db, migrate, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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

    posts = db.relationship('Post', backref='author', primaryjoin="User.id==Post.author_id")
    comments = db.relationship('Comments', backref='author', primaryjoin="User.id==Comments.author_id")

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

    def __init__(self, post_address='', title='', text=''): 
        self.post_address = post_address
        self.title = title
        self.text = text
    
    def __repr__(self):
        return f"Post('Author ID: {self.author_id}, Title: {self.title}, Date: {self.date}, Text: {self.text}')"


class Comments(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    """
    def __init__(self, text='', post=None, author=None): 
        self.text = text
        self.post_id = post.id
        self.author_id = author.id
    """
    
    def __repr__(self):
        return f"Comments('Post ID: {self.post_id}, Author ID: {self.author_id}, Date: {self.date}, Text: {self.text}')"


db.create_all()
