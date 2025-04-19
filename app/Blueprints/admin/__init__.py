from flask import (
    render_template,
    url_for,
    session,
    request,
    redirect,
    flash,
    Blueprint,
    Response,
    send_file,
)
from app import db
from sqlalchemy import String, cast
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import bulk_register_users, download_users
from app.models import User, Event, Admin
from app.forms import EventFrom
from functools import wraps
from datetime import timedelta, datetime

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


@admin.get("/dashboard")
@login_required
@admin_required
def dashboard():
    temp = session["users"] if "users" in session else None
    session["users"] = None
    column_names = [column.name for column in User.__table__.columns][:10]
    if temp is None:
        users = User.query.order_by(User.register_no).all()
        return render_template(
            "admindashboard.html",
            user=current_user,
            users=users,
            year_now=list(range(datetime.now().year, 2012, -1)),
            category=column_names,
        )
    users = []
    for user in [temp[f"{i}"] for i in range(len(temp))]:
        user = User.query.filter_by(register_no=user).first()
        users.append(user)
    return render_template(
        "admindashboard.html",
        user=current_user,
        users=users,
        year_now=list(range(datetime.now().year, 2012, -1)),
        category=column_names,
    )


@admin.get("/events")
@login_required
@admin_required
def events():

    form = EventFrom()
    events = Event.query.all()
    return render_template(
        "adminevents.html", user=current_user, form=form, events=events
    )


@admin.post("/search")
@login_required
@admin_required
def search():
    search = request.form.get("query", "")
    department = request.form.get("department", "")
    employment_status = request.form.get("employment_status", "")
    location = request.form.get("location", "")
    verified = request.form.get("verified", False)
    active = request.form.get("active", False)
    graduation_year = request.form.get("graduation_year", "")

    query = User.query

    if search:
        query = query.filter(
            (
                User.name.ilike(f"%{search}%")
                | User.email.ilike(f"%{search}%")
                | cast(User.register_no, String).ilike(f"%{search}%")
            )
        )

    if department:
        query = query.filter(User.dept == department)

    if employment_status:
        query = query.filter(User.employment_status == employment_status)

    if location:
        query = query.filter(User.location.ilike(f"%{location}%"))

    if verified:
        query = query.filter(User.approved == True)

    if active:
        query = query.filter(User.is_active == True)

    if graduation_year:
        query = query.filter(User.year == graduation_year)

    # Execute query
    users = query.order_by(User.register_no).all()

    session["users"] = dict((i, users[i].register_no) for i in range(len(users)))
    return redirect(url_for("admin.dashboard"))


@admin.get("/approve/<int:id>")
@login_required
@admin_required
def approve_user(id):
    user = User.query.filter_by(register_no=id).first()
    if user:
        if not user.approved:
            user.approved = True
            db.session.commit()
            flash("User approved", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("User already approved", "danger")
            return redirect(url_for("admin.dashboard"))
    flash("User not found", "danger")
    return redirect(url_for("admin.dashboard"))


@admin.get("/reject/<int:id>")
@login_required
@admin_required
def reject_user(id):
    user = User.query.filter_by(register_no=id).first()
    if user:
        if user.approved:
            user.approved = False
            db.session.commit()
            flash("User reject", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("User already reject", "danger")
            return redirect(url_for("admin.dashboard"))
    flash("User not found", "danger")
    return redirect(url_for("admin.dashboard"))


@admin.get("/add_users")
@login_required
@admin_required
def add_users():
    csv_path = "/home/maddy/Desktop/PROJECT/Alumni-portal-scratch/app/test/test.csv"
    result = bulk_register_users(csv_path)

    if "error" in result:
        flash(result, "danger")
        return redirect(url_for("admin.dashboard"))

    flash(result, "success")
    return redirect(url_for("admin.dashboard"))


@admin.route("/bulk_actions", methods=["POST"])
@login_required
@admin_required
def bulk_actions():
    selected_users = request.form.getlist("selected_users[]")
    action = request.form.get("action")

    if not selected_users:
        flash("No users selected", "error")
        return redirect(url_for("admin.dashboard"))
    actionslen = 0
    for user_id in selected_users:
        user = User.query.filter_by(register_no=user_id).first()
        if user:
            if action == "approve":
                if user.approved:
                    pass
                else:
                    user.approved = True
                    actionslen += 1
            elif action == "reject":
                if not user.approved:
                    pass
                else:
                    user.approved = False
                    actionslen += 1

    db.session.commit()
    flash(f"Successfully {action}d {actionslen} users", "success")
    return redirect(url_for("admin.dashboard"))


@admin.post("/download")
@login_required
@admin_required
def download():
    selected_users = request.form.getlist("selected_users[]")
    selected_fields = []
    for item in request.form.getlist("selected_fields[]"):
        cleaned = [i[1:-1] for i in item.split(",")]
        selected_fields.extend(cleaned)

    selected_fields = list(set(selected_fields))
    print(selected_fields, selected_users)
    if selected_fields and selected_users:
        if "all" in selected_fields:
            return send_file(
                download_users(selected_users),
                mimetype="text/csv",
                as_attachment=True,
                download_name="Alumni.csv",
            )
        return send_file(
            download_users(selected_users, category=selected_fields),
            mimetype="text/csv",
            as_attachment=True,
            download_name="Alumni.csv",
        )


@admin.get("/delete-all")
@login_required
@admin_required
def delete():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    flash("All users deleted successfully", "success")
    return redirect(url_for("admin.dashboard"))


@admin.post("/add_event")
@login_required
@admin_required
def add_event():
    form = EventFrom()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        expiry_date = form.date.data
        photo = form.poster.data
        mime_type = photo.mimetype
        if not title or not description or not expiry_date:
            flash("Please fill all the fields", "danger")
            return redirect(url_for("admin.events"))

        if db.session.query(Event).filter(Event.title == title).first():
            flash("Event with this title already exists", "danger")
            return redirect(url_for("admin.events"))

        event = Event(
            title=title,
            description=description,
            expiry_date=expiry_date,
            poster=photo.read(),
            mime_type=mime_type,
        )

        db.session.add(event)
        db.session.commit()
        flash("Added succeddfully", "success")
        return redirect(url_for("admin.events"))

    flash("Please fill all the fields", "danger")
    return redirect(url_for("admin.events"))


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
        return redirect(url_for("admin.events"))
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully", "success")
    return redirect(url_for("admin.events"))


@admin.post("event-edit/<int:event_id>")
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash("Event not found", "danger")
        return redirect(url_for("admin.events"))
    form = EventFrom()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.expiry_date = form.date.data
        if form.poster.data:
            event.poster = form.poster.data.read()
            event.mime_type = form.poster.data.mimetype
        else:
            event.poster = event.poster
            event.mime_type = event.mime_type
        db.session.commit()
        flash("Event updated successfully", "success")
        return redirect(url_for("admin.events"))
    return redirect(url_for("admin.events"))


@admin.route("/logout")
@login_required
@admin_required
def logout():
    if (session["next"] if "next" in session else None) == "logout":
        session["next"] = None
        return redirect(url_for("user.dash"))
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("user.loginpg"))
