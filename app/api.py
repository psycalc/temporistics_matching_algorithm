from flask import Blueprint, request, jsonify
from .services import get_types_by_typology, calculate_relationship

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/types', methods=['GET'])
def get_types_api():
    typology = request.args.get('typology')
    if not typology:
        return jsonify({'error': 'Missing typology parameter'}), 400
    types = get_types_by_typology(typology)
    if types is None:
        return jsonify({'error': f'Unknown typology: {typology}'}), 400
    return jsonify({'types': types})

@api_bp.route('/calculate', methods=['POST'])
def calculate_api():
    data = request.get_json() or {}
    user1 = data.get('user1')
    user2 = data.get('user2')
    typology = data.get('typology')

    if not user1 or not user2 or not typology:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        relationship, score = calculate_relationship(user1, user2, typology)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    return jsonify({'relationship_type': relationship, 'comfort_score': score})
