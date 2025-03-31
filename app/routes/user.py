from app import app, render_template, url_for, session, db, request, redirect, flash
from app.models import User, Event, Admin


@app.get("/")
def entry():
    return render_template("/login.html")


@app.get("/dash")
def dash():
    if "user" not in session:
        return redirect(url_for("entry"))
    query = db.select(User).where(User.register_no == session["user"])
    user = db.session.scalar(query)
    return render_template("user/dashboard.html", user=user)


@app.post("/login")
def login():
    Register_no = request.form["Register_no"]
    password = request.form["Password"]

    # Check if this is an admin login attempt (assuming admin uses email as login)
    if "@" in Register_no:  # Simple check for email format
        query = db.select(Admin).where(Admin.email == Register_no)
        admin = db.session.scalar(query)

        if admin and admin.check_password(password):
            session["user"] = None
            session["admin"] = admin.email
            flash("Welcome Admin! Login successful", "success")
            return redirect(url_for("admin_dashboard"))  # Redirect to admin dashboard

    # Regular user login
    query = db.select(User).where(User.register_no == Register_no)
    user = db.session.scalar(query)

    if user and user.check_password(password):
        session["user"] = user.register_no
        session["admin"] = None
        return redirect(url_for("dash"))

    return redirect(url_for("entry"))


@app.get("/logout")
def logout():
    session.pop("user", None)
    session.pop("admin", None)
    return redirect(url_for("entry"))


@app.post("/saveprofile")
def save_profile():
    name = request.form["name"]
    user = db.select().where(User.register_no == session["user"])
    user.name = name
    flash("Added successfully", "success")
    return redirect(url_for("dash"))
