import sys
sys.path.append("..")
from flask import current_app, Blueprint, render_template, url_for, request, flash, redirect, abort
from flask_login import login_required, current_user
from . import forms
from app import db
from app.models import User, Post, Comments
from sqlalchemy import func, update
from sqlalchemy.orm import session, sessionmaker

posts_blueprint = Blueprint('posts', __name__, template_folder='../templates/posts')


@posts_blueprint.route("/feed", methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == "POST": 
        return redirect(url_for('posts.new'))
    
    else:
        return render_template('feed.html', posts=Post.query.all())


@posts_blueprint.route("/post<post_id>", methods=['GET', 'POST'])
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
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been published.')
            return redirect(url_for('posts.posts', post_id=post_id))
        
        except Exception as e: 
            flash(f'Error while importing into DB!\n{ e }')
            return redirect(url_for('posts.posts', post_id=post_id))
    
    else:
        return render_template('posts.html', form=form, post=post, 
                                comments=comments)


@posts_blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = forms.NewPostForm()
    
    if form.validate_on_submit(): 
        title = request.form['title']
        text = request.form['text']
        
        try:
            username = current_user.username
            user = User.query.filter_by(username=username).first()
            post = Post(title=title, text=text)
            user.posts.append(post)
            db.session.commit()
            return redirect(url_for('posts.feed'))
        
        except Exception as e: 
            flash(f'Error while importing into DB!\n{ e }')
            return render_template('new.html', title='Create a post', form=form)
    
    else: 
        return render_template('new.html', title='Create a post', form=form)


@posts_blueprint.route("/post<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.username != current_user.username:
        abort(403)
    
    form = forms.NewPostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.posts', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
    
    return render_template('new.html', title='Update Post', form=form)


@posts_blueprint.route("/post<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.filter_by(post_id=post_id).all()
    
    if post.author.username != current_user.username:
        abort(403)
    
    try:
        db.session.delete(post)
        for comment in comments: 
            db.session.delete(comment)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('posts.feed'))
    
    except Exception as e:
        flash('Error while deleting from DB!', e)
        return redirect(url_for('posts.posts'))
    
