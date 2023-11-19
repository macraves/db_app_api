"""Html form objects for flask app."""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo

# from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    DateTimeField,
)


class SearchPostContent(FlaskForm):
    """Users instance, every user has its own name and unique email."""

    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Author form
class AuthorForm(FlaskForm):
    """Books row properties"""

    name = StringField("Name", validators=[DataRequired()])
    birth_date = DateTimeField("Birth Date", format="%Y-%m-%d %H:%M:%S")
    death_date = DateTimeField("Death Date", format="%Y-%m-%d %H:%M:%S")
    submit = SubmitField("Submit")


class BookForm(FlaskForm):
    """Books row properties"""

    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    condition = StringField("Condition")
    submit = SubmitField("Submit")


# Create login manager instance
class LoginForm(FlaskForm):
    """Users instance, every user has its own name and unique email."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    """Users instance, every user has its own name and unique email."""

    # variable = type(Label, parameters)
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# PostFrom class for POST method for html form
# Caution: Model properties structure has to be ordered as the form fields
class PostForm(FlaskForm):
    """Users instance, every user has its own name and unique email."""

    # variable = type(Label, parameters)
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    # it gets user_id from user table
    # author = StringField("Author", validators=[DataRequired()])
    submit = SubmitField("Submit")


# PasswordForm class for POST method for html form
class UserForm(FlaskForm):
    """Users instance, every user has its own name and unique email."""

    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password1 = PasswordField(
        "password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must be matched"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
