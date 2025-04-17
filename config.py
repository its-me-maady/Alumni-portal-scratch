import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASEURI"
    )  # or "Postgres:///" + os.path.join(basedir, "main.db")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "You won't find"
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    USE_SESSION_FOR_NEXT = True
    WTF_CSRF_ENABLED = True
