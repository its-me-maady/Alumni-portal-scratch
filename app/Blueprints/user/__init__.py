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
from app import db
from functools import wraps
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Event
from app.forms import LoginFrom, ContactForm
from datetime import timedelta

user = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="statics",
    static_url_path="statics",
)


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, User):
            for i in current_user:
                if i == None:
                    form = ContactForm()
                    flash("Please fill your details", "danger")
                    return render_template(
                        "usercontact.html", user=current_user, form=form
                    )
            return f(*args, **kwargs)
        else:
            flash("You are not authorized to view this page", "danger")
            return redirect(url_for("admin.dashboard"))

    return decorated_function


@user.get("/dash")
@login_required
@user_required
def dash():
    if not current_user.is_authenticated:
        return redirect(url_for("user.loginpg"))
    return render_template("userdashboard.html", user=current_user)


@user.route("/")
@user.route("/login", methods=["GET", "POST"])
def loginpg():
    form = LoginFrom()
    if current_user.is_authenticated:
        if isinstance(current_user, User):
            flash("You are already logged in", "danger")
            return redirect(url_for("user.dash"))
        else:
            flash("You are already logged in as admin", "danger")
            return redirect(url_for("admin.dashboard"))

    if form.validate_on_submit():
        if form.userid.data.isnumeric():
            register_no = form.userid.data
            password = form.password.data
            user = User.query.filter_by(register_no=register_no).first()
            if user and user.check_password(password):
                if not user.approved or user.date_first_login:
                    flash("Your account is not approved", "danger")
                    return redirect(url_for("user.loginpg"))
                user.last_login = db.func.now()
                db.session.commit()
                next = session["next"] if "next" in session else None
                session["next"] = None
                login_user(user, remember=True, duration=timedelta(hours=5))
                return redirect(next or url_for("user.dash"))
            else:
                flash("Invalid credentials", "danger")
                return redirect(url_for("user.loginpg"))

        else:
            session["admin.user"] = form.userid.data
            session["admin.password"] = form.password.data
            return redirect(url_for("admin.login"))

    return render_template("userlogin.html", form=form, user=current_user)


@user.get("/logout")
@login_required
@user_required
def logout():
    if (session["next"] if "next" in session else None) == "logout":
        session["next"] = None
        return redirect(url_for("user.dash"))
    logout_user()
    current_user.last_logout = db.func.now()
    db.session.commit()
    flash("Logged out successfully", "success")
    return redirect(url_for("user.loginpg"))


@user.route("/mod_profile", methods=["GET", "POST"])
@login_required
@user_required
def mod_profile():
    form = ContactForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.job_position = form.job.data
        current_user.dept = form.dept.data
        current_user.location = form.location.data
        current_user.employment_status = form.job_status.data
        current_user.year = form.year.data
        current_user.whatsapp_no = form.whatsapp_no.data
        current_user.profile = form.profile.data.read()
        current_user.mime_type = form.profile.data.mimetype
        if current_user.date_first_login is None:
            current_user.date_first_login = db.func.now()
            current_user.set_password(form.password.data)
        current_user.last_login = db.func.now()
        db.session.commit()
        flash("Added successfully", "success")
        return redirect(url_for("user.dash"))
    form.dept.data = current_user.dept
    form.year.data = str(current_user.year)
    form.job_status.data = current_user.employment_status
    if form.errors:
        flash("Please fill all the required fields", "danger")
    return render_template("usercontact.html", user=current_user, form=form)


@user.get("/events")
@login_required
@user_required
def events():
    events = Event.query.all()
    return render_template("userevents.html", events=events, user=current_user)


@user.get("/event/<int:event_id>")
@login_required
@user_required
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return Response(event.poster, mimetype=event.mime_type)


@user.get("/profile/<int:user_id>")
@login_required
@user_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return Response(user.profile, mimetype=user.mime_type)


@user.get("/event-intersted/<int:event_id>")
@login_required
@user_required
def event_interested(event_id):
    event = Event.query.get_or_404(event_id)
    if event in current_user.interested_events:
        current_user.interested_events.remove(event)
        db.session.commit()
        flash("Removed from interested events", "success")
    else:
        current_user.interested_events.append(event)
        db.session.commit()
        flash("Added to interested events", "success")
    return redirect(url_for("user.events"))
