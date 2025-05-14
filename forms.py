# Import base form class from Flask-WTF
from flask_wtf import FlaskForm

# Import different types of form fields
from wtforms import StringField, PasswordField, SubmitField, BooleanField

# Import built-in validators for checking form input
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# Import the User model to check for existing users during validation
from models import User


class RegisterForm(FlaskForm):
    # Email field (required + must be a valid email format)
    email = StringField("Email", validators=[DataRequired(), Email()])

    # Password field (required)
    password = PasswordField("Password", validators=[DataRequired()])

    # Confirm password must match the 'password' field
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )

    # Submit button
    submit = SubmitField("Register")

    # Custom validator: check if the email is already in use
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already registered.")


class LoginForm(FlaskForm):
    # Email field (required + must be valid format)
    email = StringField("Email", validators=[DataRequired(), Email()])

    # Password field (required)
    password = PasswordField("Password", validators=[DataRequired()])

    # Submit button
    submit = SubmitField("Login")


class EditAccountForm(FlaskForm):
    # Email field for updating the account (required + valid format)
    email = StringField("Email", validators=[DataRequired(), Email()])

    # Submit button
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
