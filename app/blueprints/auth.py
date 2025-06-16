from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_user, logout_user, current_user, login_required
from ..forms import RegistrationForm, LoginForm
from ..models import User, UserType
from ..extensions import db
from ..routes_helper import handle_profile_image_upload
from ..services import get_types_by_typology
from ..statistics_utils import load_typology_status
from urllib.parse import urlparse, urljoin
from flask_wtf import FlaskForm
from wtforms import HiddenField

auth_bp = Blueprint('auth', __name__)

class EmptyForm(FlaskForm):
    csrf_token = HiddenField()


def get_available_typologies():
    status = load_typology_status()
    return [name for name, enabled in status.items() if enabled]


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
    form = RegistrationForm()
    available_typologies = get_available_typologies()
    while len(form.typologies) < len(available_typologies):
        form.typologies.append_entry()

    for i, subform in enumerate(form.typologies):
        typology_name = available_typologies[i]
        subform.typology_name.data = typology_name
        available_types = get_types_by_typology(typology_name)
        if available_types:
            subform.type_value.choices = [(t, t) for t in available_types]
        else:
            subform.type_value.choices = [('No available types', 'No available types')]

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                city=form.city.data,
                country=form.country.data,
                profession=form.profession.data,
                profession_visible=form.show_profession.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)

            last_user_type = None
            for subform in form.typologies:
                ut = UserType(
                    typology_name=subform.typology_name.data,
                    type_value=subform.type_value.data,
                )
                db.session.add(ut)
                db.session.flush()
                last_user_type = ut

            if last_user_type:
                user.type_id = last_user_type.id

            if form.profile_image.data:
                if not handle_profile_image_upload(form.profile_image.data, user):
                    db.session.rollback()
                    flash('Error uploading profile image. Please try again.', 'danger')
                    return render_template('register.html', title='Register', form=form)

            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please correct the errors below and try again.', 'danger')

    return render_template('register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))
    form = LoginForm()
    google_enabled = 'google' in current_app.blueprints
    github_enabled = 'github' in current_app.blueprints
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page) if next_page else redirect(url_for('profile.index'))
        else:
            if request.method == 'POST':
                print('Form validation failed:', form.errors)
            flash('Login Unsuccessful', 'danger')
            return render_template(
                'login.html',
                title='Login',
                form=form,
                google_enabled=google_enabled,
                github_enabled=github_enabled,
            )
    return render_template(
        'login.html',
        title='Login',
        form=form,
        google_enabled=google_enabled,
        github_enabled=github_enabled,
    )


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
