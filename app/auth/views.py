import sys
sys.path.append("..")
from flask import current_app, Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from . import forms
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User, Post

auth_blueprint = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit(): 
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            try: 
                login_user(user, form.remember.data)
                flash(f'You succesfully entered into your account!')
                return redirect(url_for('posts.feed'))
            
            except Exception as e: 
                flash(f'Error while entering account!')
                flash(e)
                return render_template('login.html', form=form)
        
        else:
            flash('Login or password is not correct')
            return render_template('login.html', form=form)
    
    else: 
        return render_template('login.html', form=form)


@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit(): 
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            try:
                user = User(firstname=firstname, lastname=lastname, 
                            username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                flash(f'Account succesfully created!')
                return redirect(url_for('posts.feed'))
            
            except Exception as e:
                flash(f'Error while inserting data into DB!')
                flash(e)
                return render_template('register.html', form=form)
        
        else:
            flash('Passwords do not match!')
            return render_template('register.html', form=form)
    
    else: 
        return render_template('register.html', form=form)


@auth_blueprint.route("/forgot_password/<int:page>", methods=['GET', 'POST'])
def forgot_password(page=0, username=None):
    import random
    import string
    
    form = forms.ForgotPasswordForm()
    
    if request.method == "POST": 
        if page == 0: 
            username = request.form['username']
            
            try: 
                user = User.query.filter_by(username=username).first()
                
                if type(user) != NoneType: 
                    return redirect(url_for('auth.forgot_password', 
                                            page=1,
                                            username=username))
                
                else: 
                    flash('Oops, something went wrong!')
                    flash(e)
                    return redirect(url_for('auth.forgot_password', page=0))
            
            except Exception as e: 
                flash('Oops, something went wrong!')
                flash(e)
                return redirect(url_for('auth.forgot_password', page=0))
        
        if page == 1:
            generated_code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
            print(generated_code)
            entered_code = request.form['code']
            
            if generated_code == entered_code: 
                return redirect(url_for('auth.forgot_password', 
                                        page=2,
                                        username=username))
            
            else: 
                flash('Incorrect code!')
                return redirect(url_for('auth.forgot_password', 
                                            page=1,
                                            username=username))
        
        elif page == 2: 
            new_password = request.form['new_password']
            hash_pwd = generate_password_hash(new_password)

            try:
                current_user.password = hash_pwd
                db.session.commit()
                return redirect(url_for('user.feed'))
            
            except Exception as e:
                return redirect(url_for('auth.forgot_password', 
                                        page=2,
                                        username=username))
                    
    else: 
        return render_template('forgot_password.html', form=form, page=page)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))
