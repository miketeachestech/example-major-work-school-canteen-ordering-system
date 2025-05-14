# Import the database instance and User model
from models import db, User


def create_user(email, password, is_admin=False):
    """
    Create a user if one with the given email doesn't already exist.
    This prevents duplicate users and is useful for seeding.
    """
    # Check if a user with this email already exists in the database
    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"User '{email}' already exists.")
        return existing

    # If not, create a new user and hash the password
    user = User(email=email, is_admin=is_admin)
    user.set_password(password)  # Securely hash the password

    # Save the new user to the database
    db.session.add(user)
    db.session.commit()

    print(f"User '{email}' created.")
    return user


def seed_default_users():
    """
    Add default users to the database for testing/demo purposes.
    - One admin user
    - One regular user
    This function is called when the app first starts.
    """
    create_user("admin@example.com", "admin123", is_admin=True)
    create_user("user@example.com", "user123", is_admin=False)
