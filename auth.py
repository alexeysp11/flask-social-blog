from flask import Flask, Blueprint, render_template, url_for, request, flash, redirect
import forms
from database import User, Post
#from __name__ import app

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


@auth_blueprint.route("/forgot_password")
def forgot_password():
    form = forms.ForgotPasswordForm()

    # return forgot_password.html adding page as a parameter 
    # that can be equal euther to get_name or to get_code

    return render_template('forgot_password.html', form=form)