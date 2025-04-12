from flask import (
    render_template,
    url_for,
    session,
    request,
    redirect,
    flash,
    Blueprint,
    Response,
)
from app import db, login
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import bulk_register_users
from app.models import User, Event, Admin
from app.forms import EventFrom
from functools import wraps
from datetime import timedelta

admin = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="statics",
    static_url_path="statics",
)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, Admin):
            return f(*args, **kwargs)
        else:
            flash("You are not authorized to view this page", "danger")
            return redirect(url_for("user.dash"))

    return decorated_function


@admin.route("/")
def login():
    email = session.get("admin.user")
    password = session.get("admin.password")
    session["admin.user"] = None
    session["admin.password"] = None
    if email and password:
        user = Admin.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True, duration=timedelta(hours=5))
            return redirect(url_for("admin.dashboard"))
    flash("Invalid credentials", "danger")
    return redirect(url_for("user.loginpg"))


@admin.get("/dash")
@login_required
@admin_required
def dashboard():
    form = EventFrom()
    events = Event.query.all()
    return render_template(
        "adminevents.html", user=current_user, form=form, events=events
    )


@admin.get("/add_users")
@admin_required
@login_required
def add_users():
    csv_path = "/home/maddy/Desktop/PROJECT/Alumni-portal-scratch/app/test/test.csv"
    result = bulk_register_users(csv_path)

    if "error" in result:
        flash(result, "Danger")
        return redirect(url_for("admin.dashboard"))

    flash(result, "success")
    return redirect(url_for("admin.dashboard"))


@admin.post("/add_event")
@login_required
@admin_required
def add_event():
    form = EventFrom()
    if not form.validate_on_submit():
        flash("Please fill all the fields", "danger")
        return redirect(url_for("admin.dashboard"))
    title = form.title.data
    description = form.description.data
    expiry_date = form.date.data
    photo = form.poster.data
    mine_type = photo.mimetype
    if not title or not description or not expiry_date:
        flash("Please fill all the fields", "danger")
        return redirect(url_for("admin.events"))

    if db.session.query(Event).filter(Event.title == title).first():
        flash("Event with this title already exists", "danger")
        return redirect(url_for("admin.dashboard"))

    event = Event(
        title=title,
        description=description,
        expiry_date=expiry_date,
        poster=photo.read(),
        mime_type=mine_type,
    )

    db.session.add(event)
    db.session.commit()
    flash("Added succeddfully", "success")
    return redirect(url_for("admin.dashboard"))


@admin.get("/event/<int:event_id>")
@login_required
@admin_required
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return Response(event.poster, mimetype=event.mime_type)


@admin.get("/delete-event/<int:event_id>")
@login_required
@admin_required
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash("Event not found", "danger")
        return redirect(url_for("admin.dashboard"))
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully", "success")
    return redirect(url_for("admin.dashboard"))


@admin.get("edit-event/<int:event_id>")
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash("Event not found", "danger")
        return redirect(url_for("admin.dashboard"))
    form = EventFrom()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.expiry_date = form.date.data
        event.poster = form.poster.data.read()
        event.mime_type = form.poster.data.mimetype
        db.session.commit()
        flash("Event updated successfully", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("adminevent.html", user=current_user, form=form, event=event)


@admin.route("/logout")
@login_required
@admin_required
def logout():
    logout_user()
    return redirect(url_for("user.loginpg"))
