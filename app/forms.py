from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    FieldList,
    FormField,
    HiddenField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from wtforms.fields import FloatField  # Добавляем импорт FloatField

class TypologyTypeForm(FlaskForm):
    class Meta:
        csrf = False
        
    typology_name = HiddenField()  # Название типологии задаём в routes.py
    type_value = SelectField("Type Value", validators=[DataRequired()], choices=[])

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    typologies = FieldList(FormField(TypologyTypeForm))
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already registered. Please choose a different one.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class ProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    typology_name = StringField("Typology Name", validators=[DataRequired()])
    type_value = StringField("Type Value", validators=[DataRequired()])
    latitude = FloatField("Latitude", validators=[])
    longitude = FloatField("Longitude", validators=[])
    submit = SubmitField("Save Changes")

class EditProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    # Добавьте нужные поля для редактирования профиля
    submit = SubmitField("Save Changes")
