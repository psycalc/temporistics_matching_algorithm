from flask import Blueprint, render_template, request, jsonify
from .relationship_calculator import RelationshipCalculator
from .socionics_relationship_calculator import SocionicsRelationshipCalculator
from .typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from .services import get_types_by_typology

# Create a Blueprint for the main part of our application
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    default_typology_name = "Temporistics"
    types = get_types_by_typology(default_typology_name)
    
    if request.method == 'POST':
        typology_name = request.form.get('typology')
        user1 = request.form.get('user1')
        user2 = request.form.get('user2')
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
    
    return render_template('index.html', types=types)

# Define more routes here
@main.route('/change_language', methods=['POST'])
def change_language():
    # Your implementation here
    ...