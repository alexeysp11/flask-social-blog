from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Create DB models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    posts = db.relationship('Post', backref=db.backref('author', lazy=True), 
                            primaryjoin="User.id == Post.user_id")

    def __repr__(self):
        return f"User('{self.id}, {self.firstname}, {self.lastname}, {self.username}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_address = db.Column(db.String(30), nullable=False)
    name_of_post = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.name_of_post}, {self.date}, {self.text}')"
