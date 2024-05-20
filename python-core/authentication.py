from flask import Blueprint, request, jsonify, session
from database import register_user, validate_user

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'})

    result = register_user(email, password)
    return jsonify(result)

@auth_blueprint.route('/signin', methods=['POST'])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'})

    result = validate_user(email, password)
    if 'message' in result:
        session['email'] = email

    return jsonify(result)

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.pop('email')
        return jsonify({'message': 'Logged out successfully.'})
    else:
        return jsonify({'error': 'User not logged in.'})
