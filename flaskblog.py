from flask import Flask, render_template, url_for, request, flash, redirect
import forms
app = Flask(__name__)

app.config['SECRET_KEY'] = '3d00b8c399db2c728fcb31aff3273960'

"""
NOTE:
- you can use flask.request and flask.make_response for http authentication;
- add some error handler e.g. @app.errorhandler(404)
"""

posts = [
    {
        'author': 'Alex', 
        'title': 'Blog post 1',
        'content': 'First post content', 
        'date_posted': 'July 15, 2020'
    }, 
    {
        'author': 'Simon', 
        'title': 'Blog post 2',
        'content': 'Second post content', 
        'date_posted': 'July 15, 2020'
    }, 
    {
        'author': 'Frank', 
        'title': 'Blog post 3',
        'content': 'Third post content', 
        'date_posted': 'July 16, 2020'
    }
]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit(): 
        flash(f'You succesfully entered into your account!')
        return redirect(url_for('feed'))

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    
    if form.validate_on_submit(): 
        flash(f'Account succesfully created!')
        return redirect(url_for('feed'))
    
    return render_template('register.html', form=form)


@app.route("/forgot_password")
def forgot_password():
    form = forms.ForgotPasswordForm()
    return render_template('forgot_password.html', form=form)


@app.route("/profile")
def profile():
    return render_template('profile.html', posts=posts)


@app.route("/feed")
def feed():
    return render_template('feed.html', posts=posts)


@app.route("/new")
def new():
    form = forms.NewPostForm()
    return render_template('new.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)