from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

# You can also install 'email_validator' for email validation support!

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
    code = StringField('Code', validators=[DataRequired()])
    new_password = StringField('New password', validators=[DataRequired()])
    next_btn = SubmitField('Next')


class NewPostForm(FlaskForm):
    title = StringField('Name of Post', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    pusblish = SubmitField('Publish')


class CommentsForPostForm(FlaskForm): 
    text = TextAreaField('Comment', validators=[DataRequired()])
    pusblish = SubmitField('Publish')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    about = TextAreaField('About me')
    submit = SubmitField('Update')
