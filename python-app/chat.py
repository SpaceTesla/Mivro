# Core library imports: Flask setup
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions
from database import user_reference

# Blueprint for the chat routes
chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/load-message', methods=['POST'])
def load_message() -> Response:
    # Get email value from the incoming JSON data
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Reference the user document by email and retrieve the chat history data
        user_document = user_reference.document(email)
        user_data = user_document.get().to_dict()

        return jsonify(user_data.get('chat_history', []))
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@chat_blueprint.route('/update-message', methods=['POST'])
def update_message() -> Response:
    # Get email, index, and new message values from the incoming JSON data
    email = request.json.get('email')
    index = request.json.get('index')
    new_user_message = request.json.get('new_message')

    if not email or index is None or new_user_message is None:
        return jsonify({'error': 'Email, index, and new user message are required.'}), 400

    try:
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
    # Get email and index values from the incoming JSON data
    email = request.json.get('email')
    index = request.json.get('index')

    if not email or index is None:
        return jsonify({'error': 'Email and index are required.'}), 400

    try:
        # Reference the user document by email and delete the user message
        user_document = user_reference.document(email)
        chat_history = user_document.get().to_dict().get('chat_history', [])

        # Remove the message from the chat history
        chat_history.pop(index, None)
        user_document.update({'chat_history': chat_history})

        return jsonify({'message': 'Message deleted successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
