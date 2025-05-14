import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key used to keep session data and form submissions secure
    # In production, this should come from an environment variable
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this-is-not-secure"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB
    RESET_DB_ON_LAUNCH = False
