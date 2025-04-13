import pandas as pd
from app.models import User
from app import db


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
