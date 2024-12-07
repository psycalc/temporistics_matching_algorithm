from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    EmailField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    # Додаємо поля для вибору типології та типу
    typology_name = SelectField(
        "Typology Name",
        choices=[("Temporistics", "Temporistics"), ("Psychosophia", "Psychosophia")],
        validators=[DataRequired()],
    )
    type_value = StringField("Type Value", validators=[DataRequired()])

    submit = SubmitField("Sign Up")

    # Кастомні валідації
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is already taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is already registered. Please choose a different one."
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    typology_name = StringField("Typology Name")
    type_value = StringField("Type")
    submit = SubmitField("Save Changes")


class ProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    typology_name = StringField("Typology Name", validators=[DataRequired()])
    type_value = StringField("Type Value", validators=[DataRequired()])
    submit = SubmitField("Save Changes")
