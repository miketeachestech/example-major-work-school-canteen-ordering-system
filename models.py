# Import SQLAlchemy for database interaction
from flask_sqlalchemy import SQLAlchemy

# Import UserMixin to provide default implementations for Flask-Login
from flask_login import UserMixin

# Import Werkzeug functions for password hashing (secure storage)
from werkzeug.security import generate_password_hash, check_password_hash

# Create a SQLAlchemy database instance
db = SQLAlchemy()


class User(UserMixin, db.Model):
    # Primary key: unique ID for each user
    id = db.Column(db.Integer, primary_key=True)

    # User's email address (must be unique and not empty)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Hashed password (not the plain text password!)
    password_hash = db.Column(db.String(128), nullable=False)

    # Boolean flag to mark admin users
    is_admin = db.Column(db.Boolean, default=False)

    # Hashes the password and stores it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks if the given password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # String representation of the user object (for debugging)
    def __repr__(self):
        return f"<User {self.email}>"
