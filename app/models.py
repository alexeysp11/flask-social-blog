from app import db, migrate, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
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
    image_file = db.Column(db.String(20), nullable=False, default='default.png')

    posts = db.relationship('Post', 
                            backref='author', 
                            primaryjoin="User.id==Post.author_id")
    comments = db.relationship('Comments', 
                            backref='author', 
                            primaryjoin="User.id==Comments.author_id")
    
    
    def __init__(self, firstname='', lastname='', username='', email='', 
                 password=''): 
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        return f"User('ID: {self.id}, Firstname: {self.firstname}, Lastname: {self.lastname}, Username: {self.username}')"

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


db.create_all()
