from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from models import User, OrderStatus


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
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
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    # Custom constructor — stores the original email to compare during validation
    def __init__(self, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    # Custom validator — only raise an error if the new email is already used by someone else
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is already registered.")

class CreditForm(FlaskForm):
    email = StringField("Student Email", validators=[DataRequired(), Email()])
    amount = DecimalField("Credit Amount", validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be positive")])
    submit = SubmitField("Add Credit")

class ItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    is_vegetarian = BooleanField("Vegetarian")
    image = FileField("Item Image", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")])
    submit = SubmitField("Save Item")