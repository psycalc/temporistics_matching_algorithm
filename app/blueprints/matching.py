from flask import Blueprint, render_template, request, jsonify, current_app, flash
from flask_login import login_required
from ..services import get_types_by_typology, calculate_relationship
import openai
import os

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/get_types', methods=['GET'])
def get_types():
    typology_name = request.args.get('typology')
    types = get_types_by_typology(typology_name)
    return jsonify({'types': types})


@matching_bp.route('/calculate', methods=['POST'])
def calculate():
    user1_type = request.form.get('user1')
    user2_type = request.form.get('user2')
    typology_name = request.form.get('typology')
    if not user1_type or not user2_type or not typology_name:
        flash('Missing required parameters for calculation.', 'danger')
        return render_template('result.html', error='Missing required parameters for calculation.'), 200
    relationship_type, comfort_score = calculate_relationship(user1_type, user2_type, typology_name)
    debug = current_app.config['DEBUG']
    logs = 'Debug logs or details can be displayed here.'
    return render_template(
        'result.html',
        relationship_type=relationship_type,
        comfort_score=comfort_score,
        user1_type=user1_type,
        user2_type=user2_type,
        typology_name=typology_name,
        request_data=request.form,
        logs=logs,
        debug=debug,
    )


@matching_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')


@matching_bp.route('/chat_api', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json()
    message = data.get('message', '') if data else ''
    if not message:
        return jsonify({'reply': 'No message provided.'}), 400
    api_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return jsonify({'reply': 'OpenAI API key not configured.'})
    try:
        openai.api_key = api_key
        response = openai.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': message}],
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        current_app.logger.error(f'OpenAI error: {e}')
        reply = 'Sorry, I cannot respond right now.'
    return jsonify({'reply': reply})
