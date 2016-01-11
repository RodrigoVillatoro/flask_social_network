from flask_wtf import Form
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp
from app.models import User


class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                r'^[A-Za-z][A-Za-z0-9_.]*$',
                0,
                'Usernames can only have letters, numbers, dots or underscores'
            )]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('password2', message='Passwords must match.')
        ]
    )
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

