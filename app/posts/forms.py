from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

# You can also install 'email_validator' for email validation support!

class NewPostForm(FlaskForm):
    title = StringField('Name of Post', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    pusblish = SubmitField('Publish')


class CommentsForPostForm(FlaskForm): 
    text = TextAreaField('Comment', validators=[DataRequired()])
    pusblish = SubmitField('Publish')
