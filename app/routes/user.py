from app import app, render_template, url_for, session, db, request
from app.models import User, Event


@app.route("/")
def dash():
    return render_template("/login.html")


@app.route("/login", methods=["post"])
def login():
    Register_no = request.form["Register_no"]
    password = request.form["Password"]

    query = db.select(User).where(User.register_no == Register_no)
    user = db.session.scalar(query)
    return user
