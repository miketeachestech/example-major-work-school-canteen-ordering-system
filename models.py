from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal
from enum import Enum

class OrderStatus(Enum):
    AWAITING = "Awaiting Confirmation"
    CONFIRMED = "Confirmed"
    PREPARING = "Being Prepared"
    READY = "Ready For Pickup"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    credit = db.Column(db.Numeric(10, 2), default=0.00)

    orders = db.relationship("Order", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_credit(self, amount):
        if amount > 0:
            self.credit += Decimal(amount)

    def deduct_credit(self, amount):
        if 0 < amount <= self.credit:
            self.credit -= Decimal(amount)
            return True
        return False

    def __repr__(self):
        return f"<User {self.email}, Staff: {self.is_staff}>"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    image_filename = db.Column(db.String(255), nullable=True)

    orders = db.relationship("Order", backref="item", lazy=True)

    def __repr__(self):
        return f"<Item {self.name}, Qty: {self.quantity}, Veg: {self.is_vegetarian}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default=OrderStatus.AWAITING.value, nullable=False)

    def set_status(self, new_status: OrderStatus):
        self.status = new_status.value

    def __repr__(self):
        return f"<Order {self.id}, Item: {self.item_id}, Status: {self.status}>"
