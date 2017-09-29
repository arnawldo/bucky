from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError

from bucky.exceptions import UserNotExistsError
from bucky.models import AppManager


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(1, 24),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              "Usernames must have only letters, numbers, dots or underscores")])
    email = StringField('Email', validators=[DataRequired(), Length(1, 24), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Passwords should match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        am = AppManager().instance
        try:
            _ = am.get_user(username=field.data)
            raise ValidationError('Username already in use.')
        except UserNotExistsError:
            return None
