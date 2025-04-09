from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired


class LoginFrom(FlaskForm):
    userid = StringField("Register No", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EventFrom(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    description = StringField("Event Desciption", validators=[DataRequired()])
    date = DateField("Event Date", validators=[DataRequired()])
    poster = FileField("Event Poster", validators=[DataRequired()])
    submit = SubmitField("Submit Event", validators=[DataRequired()])
