from flask import current_app, render_template, url_for, request, flash, redirect
from flask_login import current_user
from app import app
from app import forms, db
from app.models import User, Post
from app.auth.views import auth_blueprint
from app.user.views import user_blueprint
from app.posts.views import posts_blueprint


app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(posts_blueprint)


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated: 
        return redirect(url_for('posts.feed'))
    
    else:
        return render_template('main/home.html')


@app.route("/about")
def about():
    return render_template('main/about.html')


@app.errorhandler(404)
def error404(e):
    return render_template('main/error404.html')
