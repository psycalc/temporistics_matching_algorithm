from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, SelectField,
    FieldList, FormField, HiddenField, FloatField, IntegerField
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
    username = StringField(
        _l("Username"),
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": _l("Username")}
    )
    email = StringField(
        _l("Email"),
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": _l("Email")}
    )
    password = PasswordField(
        _l("Password"),
        validators=[DataRequired()],
        render_kw={"placeholder": _l("Password")}
    )
    confirm_password = PasswordField(
        _l("Confirm Password"),
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": _l("Confirm Password")}
    )
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
    email = StringField(
        _l("Email"),
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": _l("Email")}
    )
    password = PasswordField(
        _l("Password"),
        validators=[DataRequired()],
        render_kw={"placeholder": _l("Password")}
    )
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


class WeightsForm(FlaskForm):
    temporistics = FloatField(_l("Temporistics"), default=1.0)
    psychosophia = FloatField(_l("Psychosophia"), default=1.0)
    amatoric = FloatField(_l("Amatoric"), default=1.0)
    socionics = FloatField(_l("Socionics"), default=1.0)
    submit = SubmitField(_l("Save Weights"))


class TypologyStatusForm(FlaskForm):
    temporistics_enabled = BooleanField(_l("Temporistics"), default=True)
    psychosophia_enabled = BooleanField(_l("Psychosophia"), default=True)
    amatoric_enabled = BooleanField(_l("Amatoric"), default=True)
    socionics_enabled = BooleanField(_l("Socionics"), default=True)
    submit_status = SubmitField(_l("Save Status"))


class ComfortScoreForm(FlaskForm):
    typology = SelectField(_l("Typology"), choices=[
        ('Temporistics', 'Temporistics'),
        ('Psychosophia', 'Psychosophia'),
        ('Amatoric', 'Amatoric'),
        ('Socionics', 'Socionics')
    ])
    relationship_type = StringField(_l("Relationship Type"), validators=[DataRequired()])
    score = IntegerField(_l("Score"), validators=[DataRequired()])
    submit_score = SubmitField(_l("Save Score"))
