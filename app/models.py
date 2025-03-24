from app import db, bcrypt
from datetime import datetime


user_event = db.Table(
    "user_event",
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    register_no = db.Column(db.Integer, primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    job_position = db.Column(db.String(100))
    year = db.Column(db.Integer)
    dept = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    whatsapp_no = db.Column(db.String(20), unique=True)
    photo = db.Column(db.String(255))
    date_active = db.Column(db.DateTime, default=datetime.utcnow)
    active_hours = db.Column(db.String(50))
    interested_events = db.relationship(
        "Event",
        secondary=user_event,
        back_populates="interested_users",
        overlaps="event,user",
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
    interested_users = db.relationship(
        "User",
        secondary=user_event,
        overlaps="intrested_events,user",
        back_populates="interested_events",
    )

    def is_expired(self):
        return datetime.utcnow() > self.expiry_date
