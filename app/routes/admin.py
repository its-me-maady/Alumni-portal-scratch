from app import app, render_template


@app.route("/")
def dash():
    return render_template("/admin/dash.html")
