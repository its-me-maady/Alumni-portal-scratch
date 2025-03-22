from app import db, bcrypt
from datetime import datetime


interested_users = db.Table(
    "interested_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
)


class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"Admin(id={self.id},email={self.email})"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    job_position = db.Column(db.String(100))
    year = db.Column(db.Integer, nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    whatsapp_no = db.Column(db.String(20), unique=True)
    photo = db.Column(db.String(255))
    date_active = db.Column(db.DateTime, default=datetime.utcnow)
    active_hours = db.Column(db.String(50))
    intrested_events = db.relationship(
        "event",
        secondary="interested_users",
        lazy="dynamic",
        backref=db.backref("interested_users"),
    )

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User(Name = {self.name}, email = {self.email})"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    photos = db.Column(db.String(255))

    def is_expired(self):
        return datetime.utcnow() > self.expiry_date
