from flask import render_template, request, redirect, url_for
from app import app
from app.relationship_calculator import RelationshipCalculator
from app.typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from .services import get_types_by_typology  # Import the service to get types based on typology name

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get all types from TypologyTemporistics as default, you might want to get this based on user selection
    default_typology_name = "Temporistics"
    types = get_types_by_typology(default_typology_name)
    
    if request.method == 'POST':
        typology_name = request.form['typology']
        user1 = request.form['user1']
        user2 = request.form['user2']

        # Select the correct Typology class based on user input
        typology_classes = {
            "Temporistics": TypologyTemporistics,
            "Psychosophia": TypologyPsychosophia,
            "Amatoric": TypologyAmatoric,
            "Socionics": TypologySocionics
        }
        typology_class = typology_classes.get(typology_name)

        if typology_class is None:
            # Handle the error, e.g., by returning an error message to the user
            return render_template('error.html', error_message="Invalid typology name")

        # Create a RelationshipCalculator instance and determine the relationship type and comfort score
        calculator = RelationshipCalculator(user1, user2, typology_class())
        relationship_type = calculator.determine_relationship_type()
        comfort_score = calculator.get_comfort_score(relationship_type)

        return render_template('result.html', relationship_type=relationship_type, comfort_score=comfort_score)

    # Pass the types data to the template
    return render_template('index.html', types=types)
