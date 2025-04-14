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
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileAllowed
from datetime import datetime


class LoginFrom(FlaskForm):
    userid = StringField("Register No", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EventFrom(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    description = TextAreaField("Event Desciption", validators=[DataRequired()])
    date = DateField("Event Date", validators=[DataRequired()])
    poster = FileField(
        "Event Poster",
        validators=[
            FileAllowed(["jpg", "png", "jpeg", "webp"], "Images only!"),
            Optional(),
        ],
    )
    submit = SubmitField("Submit Event", validators=[DataRequired()])


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("New Password")
    job = StringField("Current Job")
    location = StringField("Location", validators=[DataRequired()])
    dept = SelectField(
        "Department",
        choices=[
            ("Computer Science And Engineering", "Computer Science And Engineering"),
            ("Mechanical Engineering", "Mechanical Engineering"),
            ("Civil Engineering", "Civil Engineering"),
            (
                "Electrical And Electronics Engineering",
                "Electrical And Electronics Engineering",
            ),
            (
                "Electronics And Communication Engineering",
                "Electronics And Communication Engineering",
            ),
        ],
        validators=[DataRequired()],
    )
    job_status = SelectField(
        "Current status",
        choices=[
            ("Employed", "Employed"),
            ("Self Employed", "Self Employed"),
            ("Higher Studies", "Higher Studies"),
            ("Unemployed", "Unemployed"),
        ],
        validators=[DataRequired()],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    year = SelectField(
        "Graduation Year",
        choices=list(
            zip(
                range(datetime.now().year, 2012, -1),
                range(datetime.now().year, 2012, -1),
            )
        ),
        validators=[DataRequired()],
    )
    whatsapp_no = IntegerField("Whatsapp No", validators=[DataRequired()])
    profile = FileField(
        "Profile pic",
        validators=[
            FileAllowed(["jpg", "png", "jpeg", "webp"], "Images only!"),
            Optional(),
        ],
    )
    submit = SubmitField("Submit")
