import pandas as pd
from app.models import User
from app import db


def bulk_register_users(csv_path):
    """
    Registers users in bulk from a CSV file.

    Args:
        csv_path (str): Path to the CSV file containing user data.

    Returns:
        dict: A summary of the operation with counts of successes and failures.
    """
    try:
        df = pd.read_csv(csv_path, header=None)
        data = list(zip(df[0], df[1]))  # Assuming columns: register_no, password

        success_count = 0
        failure_count = 0

        for register_no, password in data:
            if not User.query.filter_by(register_no=register_no).first():
                user = User(register_no=register_no)
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
