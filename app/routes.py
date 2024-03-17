from flask import Blueprint, render_template, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .services import get_types_by_typology, cache
from .relationship_calculator import RelationshipCalculator
from .socionics_relationship_calculator import SocionicsRelationshipCalculator
from .typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from flask_wtf import FlaskForm
from wtforms import HiddenField

main = Blueprint('main', __name__)
limiter = Limiter(key_func=get_remote_address)

# Create a simple form with a hidden field for CSRF protection
class EmptyForm(FlaskForm):
    csrf_token = HiddenField()

@main.route('/get_types', methods=['GET'])
def get_types():
    typology_name = request.args.get('typology')
    types = get_types_by_typology(typology_name)
    return jsonify({'types': types})

@main.route('/', methods=['GET', 'POST'])
@limiter.limit("100/hour")
def index():
    try:
        default_typology_name = "Temporistics"
        types = get_types_by_typology(default_typology_name)
        form = EmptyForm()  # Create an instance of the form

        if request.method == 'POST':
            typology_name = request.form.get('typology')
            user1 = request.form.get('user1')
            user2 = request.form.get('user2')

            # Input validation and sanitization
            if not typology_name or not user1 or not user2:
                return render_template('error.html', error_message="Invalid input")

            typology_class = {
                "Temporistics": TypologyTemporistics,
                "Psychosophia": TypologyPsychosophia,
                "Amatoric": TypologyAmatoric,
                "Socionics": TypologySocionics
            }.get(typology_name)

            if not typology_class:
                return render_template('error.html', error_message="Invalid typology name")

            relationship_type, comfort_score = calculate_relationship(user1, user2, typology_class)
            return render_template('result.html', relationship_type=relationship_type, comfort_score=comfort_score)

        return render_template('index.html', types=types, form=form)

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return render_template('error.html', error_message="An internal server error occurred"), 500

@main.route('/change_language', methods=['POST'])
@limiter.limit("10/minute")
def change_language():
    try:
        # Remove Flask-Babel code
        return jsonify({"success": False, "error": "Language change functionality not implemented"}), 400

    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"success": False, "error": "An internal server error occurred"}), 500