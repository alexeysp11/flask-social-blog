from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)

    def __init__(self, firstname='', lastname='', username='', email='', 
                 password=''): 
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.id}, {self.firstname}, {self.lastname}, {self.username}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_address = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('posts', lazy=True))

    def __init__(self, post_address='', title='', date='', text=''): 
        self.post_address = post_address
        self.title = title
        self.date = date
        self.text = text
    
    def __repr__(self):
        return f"Post('{self.title}, {self.date}, {self.text}')"

db.create_all()
