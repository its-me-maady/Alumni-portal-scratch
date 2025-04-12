from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField,
    FileField,
    TextAreaField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired, Email


class LoginFrom(FlaskForm):
    userid = StringField("Register No", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EventFrom(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    description = TextAreaField("Event Desciption", validators=[DataRequired()])
    date = DateField("Event Date", validators=[DataRequired()])
    poster = FileField("Event Poster", validators=[DataRequired()])
    submit = SubmitField("Submit Event", validators=[DataRequired()])


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    job = StringField("Current Job", validators=[DataRequired()])
    dept = SelectField(
        "Department",
        choices=[
            ("CSE", "Computer Science And Engineering"),
            ("ME", "Mechanical Engineering"),
            ("CE", "Civil Engineering"),
            ("EE", "Electrical And Electronics Engineering"),
            ("EC", "Electronics And Communication Engineering"),
        ],
        validators=[DataRequired()],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    year = IntegerField("Batch", validators=[DataRequired()])
    whatsapp_no = IntegerField("Whatsapp No", validators=[DataRequired()])
    profile = FileField("Profile Photo", validators=[DataRequired()])
    submit = SubmitField("Submit")
