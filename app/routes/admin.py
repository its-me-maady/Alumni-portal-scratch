from app import (
    app,
    render_template,
    url_for,
    session,
    db,
    request,
    redirect,
    flash,
)
from app.utils import bulk_register_users
from app.models import Admin, User, Event


@app.get("/admin")
def admin_dashboard():
    return render_template("/admin/dashboard.html")


@app.get("/add_users")
def add_users():
    csv_path = "/home/maddy/Desktop/PROJECT/Alumni-portal-scratch/app/test/test.csv"
    result = bulk_register_users(csv_path)

    if "error" in result:
        flash(result, "Danger")
        return redirect(url_for("admin_dashboard"))

    flash(result, "success")
    return redirect(url_for("admin_dashboard"))


@app.get("/events")
def events():
    events = Event.query.all()
    return render_template("/admin/events.html", events=events)


@app.post("/add_event")
def add_event():
    flash("Added succeddfully", "success")
    return render_template("admin/events.html")
