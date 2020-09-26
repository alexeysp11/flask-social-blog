from flask import Flask, Blueprint, render_template, url_for, request, flash, redirect
import forms
from database import User, Post

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit(): 
        flash(f'You succesfully entered into your account!')
        return redirect(url_for('feed'))

    return render_template('login.html', form=form)


@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    
    if form.validate_on_submit(): 
        flash(f'Account succesfully created!')
        return redirect(url_for('feed'))
    
    return render_template('register.html', form=form)


@auth_blueprint.route("/forgot_password/<int:page>", methods=['GET', 'POST'])
def forgot_password(page):
    form = forms.ForgotPasswordForm()
    
    if request.method == "POST": 
        if page == 1:
            code = request.form['code']
        
        elif page == 2: 
            new_password = request.form['new_password']
            return redirect(url_for('feed'))
        
        else:
            username = request.form['username']
        
        page += 1
        
        return redirect(url_for('auth.forgot_password', page=page))
        
    else: 
        return render_template('forgot_password.html', form=form, page=page)

"""
@staticmethod
def make_unique_nickname(nickname):
    if User.query.filter_by(nickname=nickname).first() is None:
        return nickname
    version = 2
    while True:
        new_nickname = nickname + str(version)
        if User.query.filter_by(nickname=new_nickname).first() is None:
            break
        version += 1
    return new_nickname
"""