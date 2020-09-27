import sys
sys.path.append("..")
from flask import Flask, Blueprint, render_template, url_for, request, flash, redirect
import forms
from database import User, Post

user_blueprint = Blueprint('user', __name__, template_folder='../templates/user')


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


@user_blueprint.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username)
    
    return render_template('profile.html', username=user, posts=posts)


@user_blueprint.route("/feed", methods=['GET', 'POST'])
def feed():
    # download posts from db
    
    if request.method == "POST": 
        return render_template('new.html', form=forms.NewPostForm())
    
    else:
        return render_template('feed.html', posts=posts)


# new post
@user_blueprint.route("/new", methods=['GET', 'POST'])
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
