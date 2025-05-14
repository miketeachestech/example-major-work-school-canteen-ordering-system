import os

# Get the absolute path of the current directory (where config.py lives)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Configuration class for Flask settings
class Config:
    # Secret key used to keep session data and form submissions secure
    # In production, this should come from an environment variable
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this-is-not-secure"

    # Tells SQLAlchemy to use a SQLite database stored in app.db
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

    # Disables a feature that sends extra signals — saves memory, not needed here
    SQLALCHEMY_TRACK_MODIFICATIONS = False
