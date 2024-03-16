# services.py

from app.typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from flask import jsonify, request

def register_api_routes(app):
    @app.route('/get_types', methods=['GET'])
    def get_types():
        typology_name = request.args.get('typology')
        if not typology_name:
            return jsonify({"error": "Typology name is required"}), 400

        types = get_types_by_typology(typology_name)
        if types is None:
            return jsonify({"error": "Invalid typology name"}), 404

        return jsonify(types=types)

# Keep the function definition as it is
def get_types_by_typology(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics
    }
    typology_class = typology_classes.get(typology_name)
    if not typology_class:
        return None
    return typology_class().get_all_types()
