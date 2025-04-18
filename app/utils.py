from io import StringIO, BytesIO
from app.models import User
from app import db
import ast
import csv

def bulk_register_users(csv_path):
    with open(csv_path, "r") as file:
        try:
            data = file.readlines()
            data = [line.strip().split(",") for line in data]
            success_count = 0
            failure_count = 0

            for register_no, password in data:
                if not User.query.filter_by(register_no=register_no).first():
                    user = User(register_no=register_no, approved=True)
                    user.set_password(password)
                    db.session.add(user)
                    success_count += 1
                else:
                    failure_count += 1

            db.session.commit()
            return {"success": success_count, "failure": failure_count}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}


def download_users(
    alumni,
    category=[
        "name",
        "register_no",
        "employment_status",
        "year",
        "dept",
        "email",
        "location",
        "whatsapp_no",
    ],
):
    columns = [getattr(User, col) for col in category]
    alumni = (
        User.query.with_entities(*columns).filter(User.register_no.in_(alumni)).all()
    )
    if alumni:
        output = StringIO()
        ws = csv.writer(output)
        ws.writerow([cat.capitalize() for cat in category])
        for alumnus in alumni:
            ws.writerow(list(alumnus))
    output.seek(0)
    return BytesIO(output.getvalue().encode("utf-8"))
