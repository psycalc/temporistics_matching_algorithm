from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, SelectField,
    FieldList, FormField, HiddenField, FloatField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_babel import lazy_gettext as _l

class TypologyTypeForm(FlaskForm):
    class Meta:
        csrf = False
    typology_name = HiddenField()
    type_value = SelectField(_l("Type Value"), validators=[DataRequired()], choices=[])

class RegistrationForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    confirm_password = PasswordField(_l("Confirm Password"), validators=[DataRequired(), EqualTo("password")])
    typologies = FieldList(FormField(TypologyTypeForm))
    profile_image = FileField(_l("Profile Image"), validators=[FileAllowed(['jpg', 'png', 'jpeg'], _l('Images only!'))])
    submit = SubmitField(_l("Sign Up"))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_l("That username is already taken. Please choose a different one."))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_l("That email is already registered. Please choose a different one."))

class LoginForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Login"))

class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    typology_name = StringField(_l("Typology Name"), validators=[DataRequired()])
    type_value = StringField(_l("Type Value"), validators=[DataRequired()])
    latitude = FloatField(_l("Latitude"), validators=[DataRequired()])
    longitude = FloatField(_l("Longitude"), validators=[DataRequired()])
    max_distance = FloatField(_l("Maximum Acceptable Distance (km)"), validators=[])
    profile_image = FileField(_l("Profile Image"), validators=[FileAllowed(['jpg', 'png', 'jpeg'], _l('Images only!'))])
    submit = SubmitField(_l("Save Changes"))

class ProfileForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    typology_name = StringField(_l("Typology Name"), validators=[DataRequired()])
    type_value = StringField(_l("Type Value"), validators=[DataRequired()])
    latitude = FloatField(_l("Latitude"), validators=[])
    longitude = FloatField(_l("Longitude"), validators=[])
    max_distance = FloatField(_l("Maximum Acceptable Distance (km)"), validators=[])
    submit = SubmitField(_l("Save Changes"))

class LanguageForm(FlaskForm):
    language = SelectField(_l("Language"), choices=[
        ('en', 'English'),
        ('fr', 'Français'),
        ('es', 'Español'),
        ('uk', 'Українська')
    ])
