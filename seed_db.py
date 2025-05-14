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
    staff1 = create_user("homer@school.com", "homer123", is_staff=True)
    staff2 = create_user("marge@school.com", "marge123", is_staff=True)

    student1 = create_user("lisa@school.com", "lisa123", is_staff=False)
    student2 = create_user("bart@school.com", "bart123", is_staff=False)
    student3 = create_user("maggie@school.com", "maggie123", is_staff=False)

    return [staff1, staff2], [student1, student2, student3]



def seed_items():
    item1 = create_item("Veggie Sandwich", "4.50", 10, is_vegetarian=True)
    item1.image_filename = "veggie_sandwich.png"

    item2 = create_item("Chicken Wrap", "5.00", 8)
    item2.image_filename = "chicken_wrap.png"

    item3 = create_item("Fruit Cup", "2.00", 15, is_vegetarian=True)
    item3.image_filename = "fruit_cup.png"

    item4 = create_item("Can of Conk", "1.75", 12, is_vegetarian=True)
    item4.image_filename = "conk_can.png"

    item5 = create_item("Can of Bepis", "1.75", 10, is_vegetarian=True)
    item5.image_filename = "bepis_can.png"
    
    item6 = create_item("Hot Chips", "3.50", 5, is_vegetarian=True)
    item6.image_filename = "hot_chips.png"
    

    db.session.commit()
    return [item1, item2, item3, item4, item5, item6]



def seed_orders(students, items):
    lisa, bart, maggie = students

    create_order(lisa, items[0], 1, status=OrderStatus.COMPLETED)
    create_order(lisa, items[2], 2, status=OrderStatus.CONFIRMED)
    create_order(lisa, items[1], 1, status=OrderStatus.READY)

    create_order(bart, items[3], 2, status=OrderStatus.CANCELLED) 
    create_order(bart, items[5], 1, status=OrderStatus.AWAITING) 

    create_order(maggie, items[4], 3, status=OrderStatus.PREPARING) 
    create_order(maggie, items[0], 1, status=OrderStatus.READY)



def seed_all():
    staff, students = seed_default_users()
    items = seed_items()
    seed_orders(students, items)

    # Copy images if missing
    base_dir = os.path.dirname(__file__)
    src_dir = os.path.join(base_dir, "static", "examples")
    dest_dir = os.path.join(base_dir, "static", "uploads")
    os.makedirs(dest_dir, exist_ok=True)

    for filename in ["veggie_sandwich.png", "chicken_wrap.png", "fruit_cup.png", 
                     "conk_can.png", "bepis_can.png", "hot_chips.png", "default.png"]:
        src = os.path.join(src_dir, filename)
        dest = os.path.join(dest_dir, filename)
        if not os.path.exists(dest):
            try:
                shutil.copyfile(src, dest)
                print(f"Copied {filename} to uploads.")
            except FileNotFoundError:
                print(f"WARNING: {filename} not found in examples folder.")


