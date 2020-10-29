import sys
sys.path.append("..")
from flask import current_app, Blueprint, render_template, url_for, request, flash, redirect, abort
from flask_login import login_required, current_user
from app import forms, db
from app.models import User, Post, Comments
from sqlalchemy import func, update
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


@user_blueprint.route("/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).all()
    num_posts = len(posts)
    
    image_file = url_for('static', 
                        filename='pictures/' + user.image_file)
    
    return render_template('profile.html', 
                            image_file=image_file,
                            username=username, 
                            firstname=user.firstname, 
                            lastname=user.lastname,
                            email=user.email,
                            num_posts=num_posts,
                            posts=posts)


@user_blueprint.route("/update/<username>", methods=['GET', 'POST'])
@login_required
def update_profile(username):
    form = forms.UpdateAccountForm()
    
    if form.validate_on_submit():
        try:
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!')
            return redirect(url_for('user.profile', 
                                    username=username))
        
        except Exception as e:
            flash(f'Error while importing into DB!\n{ e }')
            db.session.rollback()
            return render_template('update_profile.html', 
                                form=form,
                                username=username)
    
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        return render_template('update_profile.html', 
                                form=form,
                                username=username)


@user_blueprint.route("/followers", methods=['GET', 'POST'])
@login_required
def followers():
    pass 


@user_blueprint.route("/followed_by", methods=['GET', 'POST'])
@login_required
def followed_by():
    pass
