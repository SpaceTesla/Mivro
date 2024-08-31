# Core library imports: Firebase Admin SDK setup
from firebase_admin import auth
from flask import Blueprint, Response, request, jsonify, redirect, url_for, session

# Local project-specific imports: Database functions
from database import register_user_profile, validate_user_profile, remove_user_profile, user_reference, runtime_error

# Blueprint for the authentication routes
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup', methods=['POST'])
def signup() -> Response:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Create a new user with the provided email and password
        auth.create_user(
            email=email,
            password=password
        )
        # Register the user in Firestore database (Workaround for Firebase Auth not supporting direct user data storage in Firestore)
        register_user_profile(email, password)
        return redirect(url_for('auth.verify_email', email=email)) # Redirect to the email verification route
    except Exception as exc:
        runtime_error('signup', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/verify-email', methods=['GET'])
def verify_email() -> Response:
    # Get the email value from the query parameters
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required for email verification.'}), 400

    try:
        # Generate an email verification link for a user in Firebase Auth using their email
        user = auth.get_user_by_email(email)
        auth.generate_email_verification_link(user.email)
        return jsonify({'message': 'Registration successful! Verify your email to activate your account.'})
    except Exception as exc:
        runtime_error('verify_email', str(exc), email=email)
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
        runtime_error('signin', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_password() -> Response:
    # Get email value from the incoming JSON data
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required for password reset.'}), 400

    try:
        # Generate a password reset link for a user in Firebase Auth using their email
        auth.generate_password_reset_link(email)
        return jsonify({'message': 'Password reset link sent successfully.'})
    except Exception as exc:
        runtime_error('reset_password', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/update-email', methods=['POST'])
def update_email() -> Response:
    # Get current email and new email values from the incoming JSON data
    current_email = request.headers.get('Mivro-Email')
    new_email = request.json.get('new_email')

    if not current_email or not new_email:
        return jsonify({'error': 'Current email and new email are required.'}), 400

    try:
        # Get the user by their current email and update their email in Firebase Auth
        user = auth.get_user_by_email(current_email)
        auth.update_user(user.uid, email=new_email)

        # Reference the user document by current email and update the email field
        current_user_document = user_reference.document(current_email)
        current_user_document.update({'account_info.email': new_email})

        # Create a new user document with the new email and delete the old one (Workdaround for Firestore not supporting document ID updates)
        new_user_document = user_reference.document(new_email)
        new_user_document.set(current_user_document.get().to_dict())
        current_user_document.delete()

        # Update the email in the session if the user is logged in
        if 'email' in session and session['email'] == current_email:
            session['email'] = new_email

        return jsonify({'message': 'Email updated successfully.'})
    except Exception as exc:
        runtime_error('update_email', str(exc), email=current_email)
        return jsonify({'error': str(exc)}), 500

@auth_blueprint.route('/logout', methods=['POST'])
def logout() -> Response:
    # Check if the user is logged in and remove their email from the session
    if 'email' in session:
        session.pop('email', None)
        return jsonify({'message': 'Logged out successfully.'})
    else:
        return jsonify({'error': 'User not logged in.'}), 401

@auth_blueprint.route('/delete-account', methods=['POST'])
def delete_account() -> Response:
    # Get email value from the request headers
    email = request.headers.get('Mivro-Email')
    if not email:
        return jsonify({'error': 'Email is required for account deletion.'}), 400

    try:
        # Check if the user's email and password are valid
        user = auth.get_user_by_email(email)
        auth.delete_user(user.uid) # Delete the user from Firebase Auth
        result = remove_user_profile(email) # Remove the user from Firestore database
        if 'error' in result:
            return jsonify(result), 500

        if 'email' in session:
            session.pop('email', None) # Remove the user's email from the session if they are logged in

        return jsonify(result)
    except Exception as exc:
        runtime_error('delete_account', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500
