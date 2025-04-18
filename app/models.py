from app import db, bcrypt, login
from datetime import datetime
from flask_login import UserMixin
from datetime import timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import desc


user_event = db.Table(
    "user_event",
    db.Column(
        "user_id", db.BigInteger, db.ForeignKey("user.register_no"), primary_key=True
    ),
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
)


class Admin(UserMixin, db.Model):
    email = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(300), nullable=False)
    __default_order__ = (desc(email),)  # Note the comma to make it a tuple

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return str(self.email)


class User(UserMixin, db.Model):
    name = db.Column(db.String(100))
    register_no = db.Column(db.BigInteger, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    job_position = db.Column(db.String(100))
    employment_status = db.Column(db.String(100))
    year = db.Column(db.Integer)
    dept = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(120))
    whatsapp_no = db.Column(db.Integer)
    profile = db.Column(db.LargeBinary)
    mime_type = db.Column(db.String(50))
    approved = db.Column(db.Boolean, default=True)
    date_first_login = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    last_logout = db.Column(db.DateTime)

    _table_args__ = (
        db.Index("idx_register_no", "register_no", unique=True),
        db.UniqueConstraint("email", name="unique_email_constraint"),
        {"extend_existing": True, "order_by": desc("register_no")},
    )

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

    def calculate_hours_logged(self):
        if self.last_logout and self.last_logout > self.last_login:
            duration = self.last_logout - self.last_login
            return int(round(duration.total_seconds() / 3600, 2))
        else:
            return 1

    @hybrid_property
    def is_active(self):
        if self.last_login < datetime.utcnow() - timedelta(days=30):
            return False
        return True

    @is_active.expression
    def is_active(cls):
        return cls.last_login > (datetime.utcnow() - timedelta(days=30))

    def get_id(self):
        return str(self.register_no)

    def __iter__(self):
        lst = [
            "name",
            "register_no",
            "employment_status",
            "year",
            "dept",
            "email",
            "location",
            "whatsapp_no",
        ]
        for attr in lst:
            yield getattr(self, attr)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    poster = db.Column(db.LargeBinary, nullable=False)
    mime_type = db.Column(db.String(50), nullable=False)
    __default_order__ = (desc(expiry_date),)  # Note the comma to make it a tuple
    interested_users = db.relationship(
        "User",
        secondary=user_event,
    )


@login.user_loader
def load_user(user_id):
    if "@" in user_id:
        return Admin.query.filter_by(email=user_id).first()
    return User.query.filter_by(register_no=user_id).first()
