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

    if "@" in Register_no:
        query = db.select(Admin).where(Admin.email == Register_no)
        admin = db.session.scalar(query)

        if admin and admin.check_password(password):
            session["user"] = None
            session["admin"] = admin.email
            flash("Welcome Admin! Login successful", "success")
            return redirect(url_for("admin_dashboard"))

        else:
            flash("Invalid credential", "danger")
            return redirect(url_for("entry"))

    query = db.select(User).where(User.register_no == Register_no)
    user = db.session.scalar(query)

    if user and user.check_password(password):
        session["user"] = user.register_no
        session["admin"] = None
        return redirect(url_for("dash"))

    else:
        flash("Invalid credential", "danger")
        return redirect(url_for("entry"))

    return redirect(url_for("entry"))


@app.get("/logout")
def logout():
    session["user"] = None
    session["admin"] = None
    return redirect(url_for("entry"))


@app.post("/mod_profile")
def mod_profile():
    name = request.form["name"]
    query = db.update(User).where(User.register_no == session["user"]).values(name=name)
    db.session.execute(query)
    db.session.commit()
    query = db.select(User).where(User.register_no == session["user"])
    print(db.session.scalar(query))
    flash("Added successfully", "success")
    return redirect(url_for("dash"))
