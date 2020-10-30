from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

# You can also install 'email_validator' for email validation support!


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
