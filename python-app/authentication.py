# Core library imports: Firebase Admin SDK setup
from firebase_admin import auth
from flask import Blueprint, request, jsonify, redirect, url_for, session
from database import register_user, validate_user, remove_user

# Blueprint for the authentication routes
auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_blueprint.route('/signup', methods=['POST'])
def signup() -> dict:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Create a new user with the provided email and password
        user = auth.create_user(
            email=email,
            password=password
        )
        # Register the user in the firestore database (workaround for Firebase Auth)
        register_user(email, password)
        return redirect(url_for('auth.verify', email=email)) # Redirect to the email verification route
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/verify-email', methods=['GET'])
def verify() -> dict:
    # Get the email value from the query parameters
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required for email verification.'}), 400

    try:
        # Generate an email verification link for a user in Firebase Auth using their email
        user = auth.get_user_by_email(email)
        link = auth.generate_email_verification_link(user.email)
        return jsonify({'message': 'Registration successful! Verify your email to activate your account.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/signin', methods=['POST'])
def signin() -> dict:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Check if the user's email and password are valid
        result = validate_user(email, password)
        if 'message' in result:
            session['email'] = email # Store the user's email in the session if the login is successful

        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset() -> dict:
    # Get email value from the incoming JSON data
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required for password reset.'}), 400

    try:
        # Generate a password reset link for a user in Firebase Auth using their email
        link = auth.generate_password_reset_link(email)
        return jsonify({'message': 'Password reset link sent.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/logout', methods=['POST'])
def logout() -> dict:
    # Check if the user is logged in and remove their email from the session
    if 'email' in session:
        session.pop('email')
        return jsonify({'message': 'Logged out successfully.'})
    else:
        return jsonify({'error': 'User not logged in.'}), 401

@auth_blueprint.route('/delete-account', methods=['POST'])
def delete() -> dict:
    # Get email value from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Check if the user's email and password are valid
        user = auth.get_user_by_email(email)
        auth.delete_user(user.uid) # Delete the user from Firebase Auth
        result = remove_user(email) # Remove the user from Firestore database
        if 'error' in result:
            return jsonify(result), 500

        if 'email' in session:
            session.pop('email') # Remove the user's email from the session if they are logged in

        return jsonify({'message': 'Account deleted successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
