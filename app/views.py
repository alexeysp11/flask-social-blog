"""
NOTE:
- you can use flask.request and flask.make_response for http authentication

>> admin = User(firstname='Admin', lastname='Admin', username='admin', email='admin@example.com', password='admin')
>>> post01 = Post(post_address='post01', title='Post 1', text='Post 2 text')
>>> db.session.add(admin)
>>> admin.posts.append(post01)
>>> db.session.commit()
"""

from flask import current_app, render_template, url_for, request, flash, redirect
from app import app
from app import forms

"""
app = Flask(__name__)
app.config['SECRET_KEY'] = '3d00b8c399db2c728fcb31aff3273960'
"""

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

"""
if __name__ == '__main__':
    app.run(debug=True)
"""