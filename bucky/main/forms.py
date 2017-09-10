from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BucketListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('Create Bucket-list')
