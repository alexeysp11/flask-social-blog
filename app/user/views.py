import sys
sys.path.append("..")
from flask import current_app, Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from app import forms, db
from app.models import User, Post, Comments
from sqlalchemy import func
from sqlalchemy.orm import session, sessionmaker

user_blueprint = Blueprint('user', __name__, template_folder='../templates/user')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@user_blueprint.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).all()
    num_posts = len(posts)
    
    image_file = url_for('static', 
                        filename='profile_pictures/' + user.image_file)
    
    return render_template('profile.html', 
                            image_file=image_file,
                            username=username, 
                            num_posts=num_posts,
                            posts=posts)


@user_blueprint.route("/update/<username>", methods=['GET', 'POST'])
@login_required
def update_profile(username):
    form = forms.UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash('Your account has been updated!', 'success')
        
        return redirect(url_for('user.profile', username=username))
    
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        
        return render_template('update_profile.html', 
                                form=form,
                                username=username)


@user_blueprint.route("/feed", methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == "POST": 
        return redirect(url_for('user.new'))
    
    else:
        return render_template('feed.html', posts=Post.query.all())


@user_blueprint.route("/posts/post<post_id>", methods=['GET', 'POST'])
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
            return redirect(url_for('user.posts', post_id=post_id))
        
        except Exception as e: 
            flash(f'Error while importing into DB!')
            flash(f'{ e }')
            return redirect(url_for('user.posts', post_id=post_id))
    
    else:
        return render_template('posts.html', form=form, post=post, 
                                comments=comments)


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
