import sys
sys.path.append("..")
from flask import current_app, Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from app import forms, db
from app.models import User, Post, Comments
from sqlalchemy.orm import session, sessionmaker


user_blueprint = Blueprint('user', __name__, template_folder='../templates/user')


@user_blueprint.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    
    return render_template('profile.html', username=username, 
                            posts=Post.query.all())


@user_blueprint.route("/feed", methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == "POST": 
        return redirect(url_for('user.new'))
    
    else:
        return render_template('feed.html', posts=Post.query.all())


@user_blueprint.route("/posts/<post_id>", methods=['GET', 'POST'])
@login_required
def posts(post_id):
    form = forms.CommentsForPostForm()
    
    post = Post.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id=post.id).all()
    
    if form.validate_on_submit(): 
        text = request.form['text']
        
        try:
            username = current_user.username
            user = User.query.filter_by(username=username).first()
            
            comment = Comments(text=text, post_id=post_id, author_id=user.id)
            
            """
            # create a configured "Session" class
            Session = sessionmaker(autoflush=False)

            # create a Session
            session = Session()

            user.comments.append(comment)
            post.comments.append(comment)
            """
            
            db.session.add(comment)
            db.session.commit()

            flash('Your comment has been published.')
            
            return redirect(url_for('user.posts', post_id=post_id))
        
        except Exception as e: 
            flash(f'Error while importing into DB!')
            flash(f'{ e }')
            
            return redirect(url_for('user.posts', post_id=post_id))
    
    else:
        return render_template('posts.html', form=form, post=post, comments=comments)


@user_blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = forms.NewPostForm()
    
    if form.validate_on_submit(): 
        post_address = request.form['post_address']
        title = request.form['title']
        text = request.form['text']
        
        try:
            username = current_user.username
            user = User.query.filter_by(username=username).first()

            post = Post(post_address=post_address, title=title, text=text)
            user.posts.append(post)
            db.session.commit()
            
            return redirect(url_for('user.feed'))
        
        except Exception as e: 
            flash(f'Error while importing into DB!')
            flash(f'{ e }')
            
            return render_template('new.html', form=form)
    
    else: 
        return render_template('new.html', form=form)


@user_blueprint.route("/followers", methods=['GET', 'POST'])
@login_required
def followers():
    pass 


@user_blueprint.route("/followed_by", methods=['GET', 'POST'])
@login_required
def followed_by():
    pass
