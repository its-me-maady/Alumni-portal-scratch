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
from datetime import timedeltav

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
            return f(*args, **kwargs)
        else:
            flash("You are not authorized to view this page", "danger")
            return redirect(url_for("admin.dashboard"))

    return decorated_function


@user.get("/dash")
@login_required
@user_required
def dash():
    form = ContactForm()
    if not current_user.is_authenticated:
        return redirect(url_for("user.loginpg"))
    return render_template("userdashboard.html", user=current_user, form=form)


@user.route("/")
@user.route("/login", methods=["GET", "POST"])
def loginpg():
    form = LoginFrom()

    if form.validate_on_submit():
        if form.userid.data.isnumeric():
            register_no = form.userid.data
            password = form.password.data
            user = User.query.filter_by(register_no=register_no).first()
            if user and user.check_password(password):
                next = session["next"] if "next" in session else None
                session["next"] = None
                login_user(user, remember=True, duration=timedelta(hours=5))
                print(current_user)
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
    if session["next"] == "logout":
        session["next"] = None
        return redirect(url_for("user.dash"))
    logout_user()
    return redirect(url_for("user.loginpg"))


@user.post("/mod_profile")
@login_required
@user_required
def mod_profile():
    name = request.form["name"]
    query = (
        db.update(User)
        .where(User.register_no == current_user.register_no)
        .values(name=name)
    )
    db.session.execute(query)
    db.session.commit()
    flash("Added successfully", "success")
    return redirect(url_for("user.dash"))


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
