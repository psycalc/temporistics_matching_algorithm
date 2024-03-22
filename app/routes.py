from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .services import get_types_by_typology, cache
from .relationship_calculator import RelationshipCalculator
from .socionics_relationship_calculator import SocionicsRelationshipCalculator
from .typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from flask_wtf import FlaskForm
from wtforms import HiddenField
from .services import calculate_relationship
from flask_babel import _
from flask import make_response
from app.forms import RegistrationForm, LoginForm
from flask import render_template, flash, redirect, url_for

main = Blueprint('main', __name__)
limiter = Limiter(key_func=get_remote_address)

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
    typology_name = request.form.get('typology')
    user1_type = request.form.get('user1')
    user2_type = request.form.get('user2')

    if not typology_name or not user1_type or not user2_type:
        return render_template('error.html', error_message=_("Invalid input. Please provide all required fields.")), 400

    typology_class = get_typology_class(typology_name)

    if not typology_class:
        return render_template('error.html', error_message=_("Invalid typology name. Please select a valid typology.")), 400

    # Validate user types
    valid_types = typology_class().get_all_types()
    if user1_type not in valid_types:
        return render_template('error.html', error_message=_("Invalid type for User 1. Please select a valid type.")), 400
    if user2_type not in valid_types:
        return render_template('error.html', error_message=_("Invalid type for User 2. Please select a valid type.")), 400

    relationship_type, comfort_score = calculate_relationship(user1_type, user2_type, typology_class)
    return render_template('result.html', relationship_type=relationship_type, comfort_score=comfort_score)

@main.route('/', methods=['GET'])
@limiter.limit("100/hour")
def index():
    try:
        default_typology_name = "Temporistics"
        types = get_types_by_typology(default_typology_name)
        form = EmptyForm()

        return render_template('index.html', types=types, form=form)

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return render_template('error.html', error_message=_("An internal server error occurred")), 500

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
    form = RegistrationForm()
    if form.validate_on_submit():
        # TODO: Add user registration logic
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: Add user login logic
        flash('You have been logged in!', 'success')
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form=form)