from app import app, render_template, url_for, session, db, request, jsonify
from app.utils import bulk_register_users
from app.models import Admin, User, Event


@app.get("/admin")
def admin_dashboard():
    return render_template("/admin/dashboard.html")


@app.post("/add_users")
def add_users():
    csv_path = "/home/maddy/Desktop/PROJECT/Alumni-portal-scratch/app/test/test.csv"
    result = bulk_register_users(csv_path)

    if "error" in result:
        return jsonify({"status": "error", "message": result["error"]}), 500

    return jsonify(
        {
            "status": "success",
            "message": f"Users added successfully. Success: {result['success']}, Failures: {result['failure']}",
        }
    )
