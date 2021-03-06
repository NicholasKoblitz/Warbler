from curses.ascii import EM
from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])



class EditUserProfileForm(FlaskForm):
    """Form for editing user profile information"""

    username = StringField("Username")
    email = StringField("Email",validators=[Email(), Optional()])
    image_url = StringField("Profile Image")
    header_image_url = StringField("Header Image")
    bio = StringField("Biography")
    password = PasswordField("Password", validators=[Length(min=6)])
