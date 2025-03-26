from app import app, render_template, url_for, session, db, request, jsonify
from app.models import Admin, User, Event
from pandas import read_csv


@app.route("/add_users")
def add_users():
    df = read_csv(
        "/home/maddy/Desktop/PROJECT/Alumni-portal-scratch/app/test/test.csv",
        header=None,
    )
    data = list(zip(df[0], df[1]))

    try:
        User.query.delete()
        for i, j in data:
            user = User(register_no=i)
            user.set_password(j)
            db.session.add(user)
            db.session.commit()
    except db.exc.IntegrityError as e:
        e = str(e).split("\n")
        print(e)
        if "(sqlite3.IntegrityError) UNIQUE constraint failed: user.register_no" in e:
            return f"This user already exist{e[2].split(",")[1]}"

    return df.to_json()
