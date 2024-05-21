from firebase_admin import auth
from flask import Blueprint, request, jsonify, redirect, url_for, session
from database import register_user, validate_user

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'})

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        register_user(email, password)
        return redirect(url_for('auth.verify', email=email))
    except Exception as exc:
        return jsonify({'error': str(exc)})

@auth_blueprint.route('/verify-email', methods=['GET'])
def verify():
    email = request.args.get('email')
    # if not email:
    #     return jsonify({'error': 'Email is required for email verification.'})

    try:
        user = auth.get_user_by_email(email)
        link = auth.generate_email_verification_link(user.email)
        return jsonify({'message': 'Registration successful. Verify your email to activate your account.'})
    except Exception as exc:
        return jsonify({'error': str(exc)})

@auth_blueprint.route('/signin', methods=['POST'])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'})

    try:
        result = validate_user(email, password)
        if 'message' in result:
            session['email'] = email

        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)})

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required for password reset.'})

    try:
        link = auth.generate_password_reset_link(email)
        return jsonify({'message': 'Password reset link sent.'})
    except Exception as exc:
        return jsonify({'error': str(exc)})

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.pop('email')
        return jsonify({'message': 'Logged out successfully.'})
    else:
        return jsonify({'error': 'User not logged in.'})
