import sys
sys.path.append("..")
from flask import current_app, Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required
from app import forms, db
#from app import db 
from app.models import User, Post

user_blueprint = Blueprint('user', __name__, template_folder='../templates/user')


@user_blueprint.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username)
    
    return render_template('profile.html', username=user, posts=Post.query.all())


@user_blueprint.route("/feed", methods=['GET', 'POST'])
@login_required
def feed():
    # download posts from db
    
    if request.method == "POST": 
        return render_template('new.html', form=forms.NewPostForm())
    
    else:
        return render_template('feed.html', posts=Post.query.all())


# new post
@user_blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = forms.NewPostForm()
    
    if form.validate_on_submit(): 
        address = Post(post_address=request.form['post_address'])
        name = Post(title=request.form['title'])
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
