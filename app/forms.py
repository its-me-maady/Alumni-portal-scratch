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
    password = PasswordField("New Password", validators=[DataRequired()])
    job = StringField("Current Job")
    location = StringField("Location", validators=[Optional()])
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
    job_status = SelectField(
        "Current status",
        choices=[
            ("employed", "Employed"),
            ("self_employed", "Self Employed"),
            ("student", "Higher Studies"),
            ("unemployed", "Unemployed"),
        ],
        validators=[DataRequired()],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    year = SelectField(
        "Graduation Year",
        choices=list(zip(range(2025, 2012, -1), range(2025, 2012, -1))),
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
