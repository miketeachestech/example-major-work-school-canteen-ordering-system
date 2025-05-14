from models import db, User, Item, Order, OrderStatus
from decimal import Decimal
import os
import shutil

def create_user(email, password, is_staff=False):
    """Create a user if one with the given email doesn't already exist."""
    existing = User.query.filter_by(email=email).first()
    if existing:
        print(f"User '{email}' already exists.")
        return existing

    user = User(email=email, is_staff=is_staff, credit=Decimal("100.00"))  # Add starting credit
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"User '{email}' created.")
    return user


def create_item(name, price, quantity, is_vegetarian=False):
    """Create an item if it doesn't already exist."""
    existing = Item.query.filter_by(name=name).first()
    if existing:
        print(f"Item '{name}' already exists.")
        return existing

    item = Item(
        name=name,
        price=Decimal(price),
        quantity=quantity,
        is_vegetarian=is_vegetarian
    )
    db.session.add(item)
    db.session.commit()
    print(f"Item '{name}' created.")
    return item


def create_order(user, item, quantity, status=OrderStatus.AWAITING):
    """Create an order for a given user and item."""
    if quantity > item.quantity:
        print(f"Not enough stock to place order for {item.name}")
        return None

    total_cost = item.price * quantity
    if user.credit < total_cost:
        print(f"User '{user.email}' does not have enough credit.")
        return None

    # Deduct stock and credit
    item.quantity -= quantity
    user.credit -= total_cost

    order = Order(
        user_id=user.id,
        item_id=item.id,
        quantity=quantity,
        total_cost=total_cost,
        status=status.value
    )

    db.session.add(order)
    db.session.commit()
    print(f"Order created: {user.email} ordered {quantity} x {item.name} ({status.value})")
    return order


def seed_default_users():
    staff = create_user("bob_staff@school.com", "bob123", is_staff=True)
    student = create_user("alice_student@school.com", "alice123", is_staff=False)
    return staff, student


def seed_items():
    item1 = create_item("Veggie Sandwich", "4.50", 10, is_vegetarian=True)
    item1.image_filename = "veggie_sandwich.png"
    item2 = create_item("Chicken Wrap", "5.00", 8)
    item2.image_filename = "chicken_wrap.png"
    item3 = create_item("Fruit Cup", "2.00", 15, is_vegetarian=True)
    item3.image_filename = "fruit_cup.png"
    db.session.commit()
    return item1, item2, item3


def seed_orders(student, items):
    create_order(student, items[0], 1, status=OrderStatus.AWAITING)
    create_order(student, items[2], 2, status=OrderStatus.CONFIRMED)
    create_order(student, items[1], 1, status=OrderStatus.READY)


def seed_all():
    staff, student = seed_default_users()
    items = seed_items()
    seed_orders(student, items)

    # Copy images if missing
    base_dir = os.path.dirname(__file__)
    src_dir = os.path.join(base_dir, "static", "examples")
    dest_dir = os.path.join(base_dir, "static", "uploads")
    os.makedirs(dest_dir, exist_ok=True)

    for filename in ["veggie_sandwich.png", "chicken_wrap.png", "fruit_cup.png"]:
        src = os.path.join(src_dir, filename)
        dest = os.path.join(dest_dir, filename)

        if not os.path.exists(dest):
            try:
                shutil.copyfile(src, dest)
                print(f"Copied {filename} to uploads.")
            except FileNotFoundError:
                print(f"WARNING: {filename} not found in examples folder.")

