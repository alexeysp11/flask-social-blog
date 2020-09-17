from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

# install 'email_validator' for email validation support!

class RegistrationForm(FlaskForm): 
    firstname = StringField('First name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Now')


class LoginForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    next_btn = SubmitField('Next')


class NewPostForm(FlaskForm):
    post_address = StringField('Post Address', validators=[DataRequired()])
    name_of_post = StringField('Name of Post', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    pusblish = SubmitField('Publish')
