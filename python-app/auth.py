# Core library imports: Firebase Admin SDK setup
from firebase_admin import auth
from flask import Blueprint, Response, request, jsonify, redirect, url_for, session

# Local project-specific imports: Database functions
from database import register_user_profile, validate_user_profile, remove_user_profile, user_reference

# Blueprint for the authentication routes
auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_blueprint.route('/signup', methods=['POST'])
def signup() -> Response:
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
        register_user_profile(email, password)
        return redirect(url_for('auth.verify', email=email)) # Redirect to the email verification route
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/verify-email', methods=['GET'])
def verify() -> Response:
    # Get the email value from the query parameters
    email = request.args.get('email')
    # if not email:
    #     return jsonify({'error': 'Email is required for email verification.'}), 400

    try:
        # Generate an email verification link for a user in Firebase Auth using their email
        user = auth.get_user_by_email(email)
        link = auth.generate_email_verification_link(user.email)
        return jsonify({'message': 'Registration successful! Verify your email to activate your account.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/signin', methods=['POST'])
def signin() -> Response:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Check if the user's email and password are valid
        result = validate_user_profile(email, password)
        if 'message' in result:
            session['email'] = email # Store the user's email in the session if the login is successful

        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset() -> Response:
    # Get email value from the incoming JSON data
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required for password reset.'}), 400

    try:
        if auth.get_user_by_email(email):
            # Generate a password reset link for a user in Firebase Auth using their email
            link = auth.generate_password_reset_link(email)
            return jsonify({'message': 'Password reset link sent.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/update-email', methods=['POST'])
def update_email() -> Response:
    # Get current email, new email, and password from the incoming JSON data
    current_email = request.json.get('current_email')
    new_email = request.json.get('new_email')
    password = request.json.get('password')
    if not current_email or not new_email or not password:
        return jsonify({'error': 'Current email, new email, and password are required.'}), 400

    try:
        # Validate the user's current credentials
        result = validate_user_profile(current_email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Get the user by their current email and update their email in Firebase Auth
        user = auth.get_user_by_email(current_email)
        auth.update_user(user.uid, email=new_email)

        # Reference the user document by current email and update the email field
        user_document = user_reference.document(current_email)
        user_document.update({'account_info.email': new_email})

        # Create a new user document with the new email and delete the old one
        new_user_document = user_reference.document(new_email)
        new_user_document.set(user_document.get().to_dict())
        user_document.delete()

        # Update the email in the session if the user is logged in
        if 'email' in session and session['email'] == current_email:
            session['email'] = new_email

        return jsonify({'message': 'Email updated successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/logout', methods=['POST'])
def logout() -> Response:
    # Check if the user is logged in and remove their email from the session
    if 'email' in session:
        session.pop('email')
        return jsonify({'message': 'Logged out successfully.'})
    else:
        return jsonify({'error': 'User not logged in.'}), 401

@auth_blueprint.route('/delete-account', methods=['POST'])
def delete() -> Response:
    # Get email value from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Check if the user's email and password are valid
        user = auth.get_user_by_email(email)
        auth.delete_user(user.uid) # Delete the user from Firebase Auth
        result = remove_user_profile(email) # Remove the user from Firestore database
        if 'error' in result:
            return jsonify(result), 500

        if 'email' in session:
            session.pop('email') # Remove the user's email from the session if they are logged in

        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
