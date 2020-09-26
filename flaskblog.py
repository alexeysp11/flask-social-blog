"""
NOTE:
- you can use flask.request and flask.make_response for http authentication
"""

from flask import Flask, render_template, url_for, request, flash, redirect
import forms
from database import User, Post


app = Flask(__name__)
app.config['SECRET_KEY'] = '3d00b8c399db2c728fcb31aff3273960'

from auth import auth_blueprint
app.register_blueprint(auth_blueprint)

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
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/profile")
def profile():
    return render_template('profile.html', posts=posts)


@app.route("/feed", methods=['GET', 'POST'])
def feed():
    # download posts from db
    
    if request.method == "POST": 
        return render_template('new.html', form=forms.NewPostForm())
    
    else:
        return render_template('feed.html', posts=posts)


# new post
@app.route("/new", methods=['GET', 'POST'])
def new():
    form = forms.NewPostForm()
    
    if form.validate_on_submit(): 
        address = Post(post_address=request.form['post_address'])
        name = Post(name_of_post=request.form['name_of_post'])
        text = Post(text=request.form['text'])

        try:
            db.session.add(address)
            db.session.add(name)
            db.session.add(text)

            db.session.commit()
            
            return redirect(url_for('feed'))
        
        except:
            flash(f'Try again!')
            return render_template('new.html', form=form)
    
    else: 
        return render_template('new.html', form=form)


@app.errorhandler(404)
def error404(e):
    return render_template('error404.html')


if __name__ == '__main__':
    app.run(debug=True)