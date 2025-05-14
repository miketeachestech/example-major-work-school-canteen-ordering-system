from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from models import db, User, Item
from forms import RegisterForm, LoginForm, EditAccountForm, CreditForm, ItemForm
from config import Config
from seed_db import seed_all

app = Flask(__name__)
app.config.from_object(Config)  # Load settings like SECRET_KEY and DB path

db.init_app(app)

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect to this route if login is required


@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for session tracking (used by Flask-Login)."""
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    """Redirect users from the home page to the dashboard."""
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user.
    - Redirects to dashboard if already logged in.
    - Saves user to the database if form is valid.
    """
    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard")
        )  # Don't allow already logged-in users to register again

    form = RegisterForm()
    # If the form was submitted (POST request) and passed all validation checks
    if form.validate_on_submit():
        # Create a new user and save to the database
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in an existing user.
    - Redirects to dashboard if already logged in.
    - Authenticates credentials and logs in the user.
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists and password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """Log out the current user and redirect to the login page."""
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard page for logged-in users."""
    return render_template("dashboard.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """
    Allow the logged-in user to update their email.
    - Shows a form prefilled with the current email.
    - Validates and saves new email if submitted.
    """
    # Prefill form with the current user's email
    form = EditAccountForm(original_email=current_user.email)
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.email.data = current_user.email  # Fill in the email when the page loads
    return render_template("edit_account.html", form=form)


@app.route("/users")
@login_required
def users():
    """
    Staff-only view of all registered users.
    - Redirects non-staffs back to dashboard.
    """
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    # Show a list of all users in the system
    all_users = User.query.all()
    return render_template("users.html", users=all_users)


@app.route("/credit", methods=["GET", "POST"])
@login_required
def credit():
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    form = CreditForm()
    if form.validate_on_submit():
        student = User.query.filter_by(email=form.email.data, is_staff=False).first()
        if not student:
            flash("Student not found or this person is not a student.", "danger")
        else:
            student.add_credit(form.amount.data)
            db.session.commit()
            flash(f"Added ${form.amount.data:.2f} to {student.email}'s account.", "success")
            return redirect(url_for("credit"))
    return render_template("credit.html", form=form)

@app.route("/items")
@login_required
def items():
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    all_items = Item.query.all()
    return render_template("items.html", items=all_items)


@app.route("/items/add", methods=["GET", "POST"])
@login_required
def add_item():
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            price=form.price.data,
            quantity=form.quantity.data,
            is_vegetarian=form.is_vegetarian.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Item added successfully.", "success")
        return redirect(url_for("items"))
    return render_template("item_form.html", form=form, action="Add")


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.quantity = form.quantity.data
        item.is_vegetarian = form.is_vegetarian.data
        db.session.commit()
        flash("Item updated successfully.", "success")
        return redirect(url_for("items"))
    return render_template("item_form.html", form=form, action="Edit")


@app.route("/items/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully.", "success")
    return redirect(url_for("items"))

if __name__ == "__main__":
    """
    Initialize the database, seed default users, and start the development server.
    This block runs only when this file is executed directly (not imported), i.e. "python app.py".
    """
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        seed_all()  # Add default staff and regular users

    app.run(debug=True)  # Start the server with debug mode (auto-reloads on changes)
