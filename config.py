import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASEURI"
    ) or "sqlite:///" + os.path.join(basedir, "main.db")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "You won't find"
    USE_SESSION_FOR_NEXT = True
    WTF_CSRF_ENABLED = True
