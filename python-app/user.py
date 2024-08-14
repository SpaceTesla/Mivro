# Core library imports: Firebase Admin SDK setup
from firebase_admin import auth
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions and models
from database import save_health_profile
from models import HealthProfile

# Blueprint for the user routes
user_blueprint = Blueprint('user', __name__, url_prefix='/api/v1/user')

@user_blueprint.route('/submit-health-profile', methods=['POST'])
def submit_health_profile() -> Response:
    # Get email from the incoming JSON request
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Check if the user exists in Firebase Auth
        if not auth.get_user_by_email(email):
            return jsonify({'error': 'User not found.'}), 404

        # Create an instance of HealthProfile using the request data
        health_data = HealthProfile(
            age=request.json.get('age'),
            gender=request.json.get('gender'),
            height=request.json.get('height'),
            weight=request.json.get('weight'),
            dietary_preferences=request.json.get('dietary_preferences'),
            allergies=request.json.get('allergies'),
            medical_conditions=request.json.get('medical_conditions')
        )

        # Store the health profile data for the user in Firestore
        result = save_health_profile(email, health_data.to_dict())
        if 'error' in result:
            return jsonify(result), 500

        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
