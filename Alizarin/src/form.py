from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from . import db
from .model.user import User


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    firstname = StringField('First name', validators=[Length(1, 10)])
    lastname = StringField('Last name', validators=[Length(1, 20)])

    email = StringField('Email', [
        Email(message='Invalid email address'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password"),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm password', validators=[
        Length(min=6, max=10)
    ])

    submit = SubmitField('Submit')



class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Invalid email address'),
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired(message="Please enter a password")])

    submit = SubmitField('Submit')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password')


class ProjectForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Project name', validators=[Length(1, 32)])
    submit = SubmitField('Create project')


class SprintForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Sprint name', validators=[Length(1, 32)])
    submit = SubmitField('Create sprint')


class TaskForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Task name', validators=[Length(1, 32)])
    description = TextAreaField('Sprint description', validators=[Length(1, 1024)])
    submit = SubmitField('Add task to sprint')


class UserForm(FlaskForm):
    class Meta:
        csrf = False
    email = StringField('Email', [Email(message='Invalid email address.'), DataRequired()])
    submit = SubmitField('Add project user')


class UserStory(FlaskForm):
    class Meta:
        csrf = False
    content = TextAreaField('Story description', validators=[Length(1, 1024)])
    submit = SubmitField('Create user story')
