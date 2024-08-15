# Core library imports: Flask setup
from flask import request, jsonify

# Local project-specific imports: Database functions
from database import validate_user_profile

def authenticate():
    # Allow OPTIONS requests to pass through
    if request.method == 'OPTIONS':
        return None # Skip authentication for OPTIONS requests

    # List of routes that do not require authentication
    unrestricted_routes = [
        '/api/v1/auth/signup',
        '/api/v1/auth/verify-email',
        '/api/v1/auth/signin',
        '/api/v1/auth/reset-password'
    ]

    if request.path in unrestricted_routes:
        return None # Skip authentication for unrestricted routes

    # Get email and password values from the request headers
    email = request.headers.get('Mivro-Email')
    password = request.headers.get('Mivro-Password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 401

    try:
        # Validate the user profile using the email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            # Set the status code based on the error message
            status_code = 401 if 'Incorrect password' in result['error'] else 404
            return jsonify(result), status_code
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
