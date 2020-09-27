"""
NOTE:
- you can use flask.request and flask.make_response for http authentication
"""

from flask import Flask, render_template, url_for, request, flash, redirect
import forms
from database import User, Post


app = Flask(__name__)
app.config['SECRET_KEY'] = '3d00b8c399db2c728fcb31aff3273960'


from auth.views import auth_blueprint
from user.views import user_blueprint

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


if __name__ == '__main__':
    app.run(debug=True)