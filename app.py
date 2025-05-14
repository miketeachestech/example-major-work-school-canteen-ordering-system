from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from models import db, User, Item, Order, OrderStatus
from forms import (
    RegisterForm,
    LoginForm,
    EditAccountForm,
    CreditForm,
    ItemForm,
    OrderForm,
)
from config import Config
from seed_db import seed_all
import os
import uuid
from werkzeug.utils import secure_filename
from helpers import get_next_status


app = Flask(__name__)
app.config.from_object(Config)  # Load settings like SECRET_KEY and DB path

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    form = EditAccountForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "danger")
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Your password has been updated.", "success")
            return redirect(url_for("account"))

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
            flash(
                f"Added ${form.amount.data:.2f} to {student.email}'s account.",
                "success",
            )
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
        filename = None
        if form.image.data:
            original_name = secure_filename(form.image.data.filename)
            ext = os.path.splitext(original_name)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            form.image.data.save(image_path)

        item = Item(
            name=form.name.data,
            price=form.price.data,
            quantity=form.quantity.data,
            is_vegetarian=form.is_vegetarian.data,
            image_filename=filename,
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
        # Store old filename BEFORE updating it
        old_filename = item.image_filename

        if form.image.data:
            # Delete old image if it exists
            if old_filename:
                old_path = os.path.join(UPLOAD_FOLDER, old_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

            # Save new image
            original_name = secure_filename(form.image.data.filename)
            ext = os.path.splitext(original_name)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            form.image.data.save(image_path)
            item.image_filename = filename

        # Update other fields
        item.name = form.name.data
        item.price = form.price.data
        item.quantity = form.quantity.data
        item.is_vegetarian = form.is_vegetarian.data

        db.session.commit()
        flash("Item updated successfully.", "success")
        return redirect(url_for("items"))

    return render_template("item_form.html", form=form, action="Edit")


@app.errorhandler(413)
def file_too_large(error):
    flash("File is too large (max 2MB).", "danger")
    return redirect(request.referrer or url_for("dashboard"))


@app.route("/items/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    item = Item.query.get_or_404(item_id)

    # Delete associated image if it exists
    if item.image_filename:
        image_path = os.path.join(UPLOAD_FOLDER, item.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully.", "success")
    return redirect(url_for("items"))


@app.route("/orders", methods=["GET", "POST"])
@login_required
def manage_orders():
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    # Split orders
    active_statuses = {
        OrderStatus.AWAITING.value,
        OrderStatus.CONFIRMED.value,
        OrderStatus.PREPARING.value,
        OrderStatus.READY.value,
    }

    active_orders = (
        Order.query.filter(Order.status.in_(active_statuses))
        .order_by(Order.timestamp.desc())
        .all()
    )

    # Pagination
    page = request.args.get("page", 1, type=int)
    closed_statuses = [OrderStatus.COMPLETED.value, OrderStatus.CANCELLED.value]
    closed_orders_pagination = (
        Order.query.filter(Order.status.in_(closed_statuses))
        .order_by(Order.timestamp.desc())
        .paginate(page=page, per_page=5)
    )

    if request.method == "POST":
        order_id = int(request.form["order_id"])
        action = request.form["action"]
        order = Order.query.get_or_404(order_id)

        if action == "advance":
            next_status = get_next_status(order.status)
            if order.status != next_status:
                order.status = next_status
                flash(f"Order #{order.id} advanced to '{next_status}'.", "success")
        elif action == "cancel" and order.status != OrderStatus.CANCELLED.value:
            order.status = OrderStatus.CANCELLED.value
            order.user.credit += order.total_cost
            order.item.quantity += order.quantity
            flash(
                f"Order #{order.id} cancelled. Credit refunded and stock restored.",
                "warning",
            )

        db.session.commit()
        return redirect(url_for("manage_orders", page=page))

    return render_template(
        "manage_orders.html",
        active_orders=active_orders,
        closed_orders_pagination=closed_orders_pagination,
    )


@app.route("/users/<int:user_id>/promote", methods=["POST"])
@login_required
def promote_user(user_id):
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)

    if user.is_staff:
        flash("User is already a staff member.", "info")
    else:
        user.is_staff = True
        db.session.commit()
        flash(f"User '{user.email}' has been promoted to staff.", "success")

    return redirect(url_for("users"))


@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_staff:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("users"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.email}' has been deleted.", "warning")
    return redirect(url_for("users"))


@app.route("/store")
@login_required
def store():
    if current_user.is_staff:
        flash("Store is for students only.", "info")
        return redirect(url_for("dashboard"))

    # Read filter parameters from query string
    name = request.args.get("name", "").strip()
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    min_quantity = request.args.get("min_quantity", type=int)
    is_vegetarian = request.args.get("is_vegetarian") == "on"

    # Base query
    query = Item.query.filter(Item.quantity > 0)

    if name:
        query = query.filter(Item.name.ilike(f"%{name}%"))
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    if min_quantity is not None:
        query = query.filter(Item.quantity >= min_quantity)
    if is_vegetarian:
        query = query.filter(Item.is_vegetarian == True)

    items = query.order_by(Item.name).all()
    return render_template("store.html", items=items)


@app.route("/order/<int:item_id>", methods=["GET", "POST"])
@login_required
def order_item(item_id):
    if current_user.is_staff:
        flash("Only students can place orders.", "danger")
        return redirect(url_for("dashboard"))

    item = Item.query.get_or_404(item_id)

    if item.quantity <= 0:
        flash("This item is currently out of stock.", "warning")
        return redirect(url_for("store"))

    form = OrderForm()
    if form.validate_on_submit():
        qty = form.quantity.data

        if qty > item.quantity:
            flash(f"Only {item.quantity} of '{item.name}' available.", "danger")
        else:
            total_cost = item.price * qty
            if current_user.credit < total_cost:
                flash("Insufficient credit to place this order.", "danger")
            else:
                # Update stock and credit
                item.quantity -= qty
                current_user.credit -= total_cost

                order = Order(
                    user_id=current_user.id,
                    item_id=item.id,
                    quantity=qty,
                    total_cost=total_cost,
                    status=OrderStatus.AWAITING.value,
                )

                db.session.add(order)
                db.session.commit()
                flash("Order placed successfully!", "success")
                return redirect(url_for("store"))

    return render_template("order_item.html", item=item, form=form)


@app.route("/my-orders")
@login_required
def my_orders():
    if current_user.is_staff:
        flash("Staff accounts do not place orders.", "info")
        return redirect(url_for("dashboard"))

    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.timestamp.desc())
        .all()
    )
    return render_template("my_orders.html", orders=orders)


@app.context_processor
def inject_nav_data():
    from models import Order, OrderStatus

    if current_user.is_authenticated:
        if current_user.is_staff:
            active_statuses = {
                OrderStatus.AWAITING.value,
                OrderStatus.CONFIRMED.value,
                OrderStatus.PREPARING.value,
                OrderStatus.READY.value,
            }
            active_order_count = Order.query.filter(
                Order.status.in_(active_statuses)
            ).count()
            return {"active_order_count": active_order_count}
        else:
            return {"student_credit": current_user.credit}
    return {}


if __name__ == "__main__":
    """
    Initialize the database, seed default users, and start the development server.
    This block runs only when this file is executed directly (not imported), i.e. "python app.py".
    """
    with app.app_context():
        reset_db_on_launch = Config.RESET_DB_ON_LAUNCH
        if reset_db_on_launch:
            db.drop_all()
            db.create_all()
            seed_all()
            print("Database was reset successfully.")
        else:
            db.create_all()
            print("Database reset skipped.")

    app.run(debug=True)
