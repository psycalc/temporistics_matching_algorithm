from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, ProfileForm, EditProfileForm
from .models import User, UserType
from . import db, login_manager
from .services import get_types_by_typology, calculate_relationship
from .typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from flask_wtf import FlaskForm
from wtforms import HiddenField
from urllib.parse import urlparse, urljoin

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class EmptyForm(FlaskForm):
    csrf_token = HiddenField()

@main.route('/get_types', methods=['GET'])
def get_types():
    typology_name = request.args.get('typology')
    types = get_types_by_typology(typology_name)
    return jsonify({'types': types})

def get_typology_class(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics
    }
    return typology_classes.get(typology_name)

@main.route('/calculate', methods=['POST'])
def calculate():
    user1_type = request.form.get('user1')
    user2_type = request.form.get('user2')
    typology_name = request.form.get('typology')
    relationship_type, comfort_score = calculate_relationship(user1_type, user2_type, typology_name)

    debug = current_app.config['DEBUG']
    logs = "Debug logs or details can be displayed here."

    return render_template('result.html', 
                           relationship_type=relationship_type,
                           comfort_score=comfort_score,
                           user1_type=user1_type,
                           user2_type=user2_type,
                           typology_name=typology_name,
                           request_data=request.form,
                           logs=logs,
                           debug=debug)

@main.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        default_typology_name = "Temporistics"
        types = get_types_by_typology(default_typology_name)
        form = EmptyForm()
        return render_template('index.html', types=types, form=form)
    else:
        return redirect(url_for('main.login'))

@main.route('/change_language', methods=['POST'])
def change_language():
    COOKIE_NAME = 'locale'
    COOKIE_EXPIRATION = 60 * 60 * 24 * 30  # 30 days

    language = request.form.get('language')
    if language and language in current_app.config['LANGUAGES']:
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie(COOKIE_NAME, language, max_age=COOKIE_EXPIRATION)
        return response
    else:
        current_app.logger.error(f"Failed to change language. Supported languages: {current_app.config['LANGUAGES']}")
        return jsonify({"success": False, "error": "Language change failed. Please select a supported language."}), 400

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        user_type = UserType(typology_name=form.typology_name.data, type_value=form.type_value.data, user=user)
        db.session.add(user)
        db.session.add(user_type)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user != current_user:
        flash('You do not have permission to view or edit this profile.', 'danger')
        return redirect(url_for('main.index'))

    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.typology_name = form.typology_name.data
        user.type_value = form.type_value.data
        try:
            db.session.commit()
            flash('Profile updated successfully.', 'success')
        except:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')

        return redirect(url_for('main.user_profile', username=user.username))

    return render_template('profile.html', user=user, form=form)
