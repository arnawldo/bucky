from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 24), Regexp('^[a-z0-9_-]{1, 24}')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 24), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')
