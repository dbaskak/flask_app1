from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    date = DateTimeField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
