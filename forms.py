from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    DecimalField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
    Length,
)
from models import User, OrderStatus


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )

    submit = SubmitField("Register")

    # Custom validator: check if the email is already in use
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditAccountForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Update Password")


class CreditForm(FlaskForm):
    email = StringField("Student Email", validators=[DataRequired(), Email()])
    amount = DecimalField(
        "Credit Amount",
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message="Amount must be positive"),
        ],
    )
    submit = SubmitField("Add Credit")


class ItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    is_vegetarian = BooleanField("Vegetarian")
    image = FileField(
        "Item Image", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")]
    )
    submit = SubmitField("Save Item")


class OrderForm(FlaskForm):
    quantity = IntegerField(
        "Quantity",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Quantity must be at least 1"),
        ],
    )
    submit = SubmitField("Place Order")
