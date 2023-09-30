from app.typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics
from app import app
from flask import jsonify, request

def get_types_by_typology(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics
    }
    typology_class = typology_classes.get(typology_name, TypologyTemporistics)  # Default to TypologyTemporistics
    return typology_class().get_all_types()

@app.route('/get_types', methods=['GET'])
def get_types():
    typology_name = request.args.get('typology')
    types = get_types_by_typology(typology_name)
    return jsonify(types=types)
