from firebase_admin import auth
from flask import Blueprint, Response, request, jsonify, redirect, url_for

from database import save_health_profile
from models import HealthProfile

chat_blueprint = Blueprint('chat', __name__, url_prefix='/api/v1/chat')

@chat_blueprint.route('/submit-health-profile', methods=['POST'])
def health_profile() -> Response:
    # Get email from the incoming JSON request
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    # Create an instance of HealthProfile using the request data
    profile = HealthProfile(
        age=request.json.get('age'),
        gender=request.json.get('gender'),
        height=request.json.get('height'),
        weight=request.json.get('weight'),
        dietary_preferences=request.json.get('dietary_preferences', []),
        allergies=request.json.get('allergies', []),
        medical_conditions=request.json.get('medical_conditions', [])
    )

    try:
        # Check if the user exists in Firebase Auth
        if auth.get_user_by_email(email):
            # Save the health profile data to the database
            result = save_health_profile(email, profile.to_dict())
            return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500