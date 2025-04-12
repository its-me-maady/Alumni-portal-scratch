from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = "user.loginpg"

login.login_message = "Please log in to access this page."
login.login_message_category = "info"


from app.Blueprints.admin import admin
from app.Blueprints.user import user


app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/user")


@app.route("/")
def index():
    return redirect(url_for("user.loginpg"))
