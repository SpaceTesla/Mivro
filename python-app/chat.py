# Core library imports: Flask setup
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions
from database import user_reference, validate_user_profile

# Blueprint for the chat routes
chat_blueprint = Blueprint('chat', __name__, url_prefix='/api/v1/chat')

@chat_blueprint.route('/load-message', methods=['POST'])
def load_message() -> Response:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and retrieve the chat history data
        user_document = user_reference.document(email)
        user_data = user_document.get().to_dict()
        return jsonify(user_data.get('chat_history', []))
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@chat_blueprint.route('/update-message', methods=['POST'])
def update_message() -> Response:
    # Get email, password, index, and new_user_message values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    index = request.json.get('index')
    new_user_message = request.json.get('new_user_message')

    if not email or not password or index is None or new_user_message is None:
        return jsonify({'error': 'Email, password, index, and new_user_message are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and update the user message
        user_document = user_reference.document(email)
        chat_history = user_document.get().to_dict().get('chat_history', [])

        # Store the new user message in the chat history
        chat_history[index]['user_message'] = new_user_message
        user_document.update({'chat_history': chat_history})

        return jsonify({'message': 'Message updated successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@chat_blueprint.route('/delete-message', methods=['POST'])
def delete_message() -> Response:
    # Get email, password, and index values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')
    index = request.json.get('index')

    if not email or not password or index is None:
        return jsonify({'error': 'Email, password, and index are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and delete the user message
        user_document = user_reference.document(email)
        chat_history = user_document.get().to_dict().get('chat_history', [])

        # Remove the message from the chat history
        chat_history.pop(index)
        user_document.update({'chat_history': chat_history})

        return jsonify({'message': 'Message deleted successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
