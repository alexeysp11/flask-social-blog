from flask import current_app, render_template, url_for, request, flash, redirect
from app import app
from app import forms
from app.auth.views import auth_blueprint
from app.user.views import user_blueprint


app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.errorhandler(404)
def error404(e):
    return render_template('error404.html')
