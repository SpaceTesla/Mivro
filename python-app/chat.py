# Core library imports: Flask setup
import requests
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions
from database import user_reference, runtime_error

# Blueprint for the chat routes
chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/load-message', methods=['POST'])
def load_message() -> Response:
    # Get email value from the request headers
    email = request.headers.get('Mivro-Email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Reference the user document by email and retrieve the chat history data
        user_document = user_reference.document(email)
        user_data = user_document.get().to_dict()
        return jsonify(user_data.get('chat_history', []))
    except Exception as exc:
        runtime_error('load_message', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@chat_blueprint.route('/update-message', methods=['POST'])
def update_message() -> Response:
    # Get email, old message, and new message values from the incoming JSON data
    email = request.headers.get('Mivro-Email')
    old_message = request.json.get('old_message')
    new_message = request.json.get('new_message')

    if not email or not old_message or not new_message:
        return jsonify({'error': 'Email, old message, and new message are required.'}), 400

    try:
        # Reference the user document by email and retrieve the chat history
        user_document = user_reference.document(email)
        chat_history = user_document.get().to_dict().get('chat_history', [])

        # Delete the old message from the chat history
        new_chat_history = [
            record for record in chat_history
            if record.get('user_message') != old_message
        ]

        # Check if the old message was found and deleted
        if len(new_chat_history) == len(chat_history):
            return jsonify({'error': 'Old message not found in chat history.'}), 404

        # Save the updated chat history to the database after deleting the old message
        user_document.update({'chat_history': new_chat_history})
        # Send the new message to the Savora AI model for processing and return the response
        savora_response = requests.post(
            'http://localhost:5000/api/v1/ai/savora',
            headers={'Mivro-Email': email, 'Mivro-Password': request.headers.get('Mivro-Password')},
            json={'type': 'text', 'message': new_message}
        )

        if savora_response.status_code != 200:
            runtime_error('update_message', 'Savora AI failed to process the message.', middleware=savora_response.json(), email=email)
            return jsonify({'error': 'Savora AI failed to process the message.'}), savora_response.status_code

        return savora_response.json()
    except Exception as exc:
        runtime_error('update_message', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@chat_blueprint.route('/delete-message', methods=['POST'])
def delete_message() -> Response:
    # Get email and delete message values from the incoming JSON data
    email = request.headers.get('Mivro-Email')
    delete_message = request.json.get('delete_message')

    if not email or not delete_message:
        return jsonify({'error': 'Email and delete message are required.'}), 400

    try:
        # Reference the user document by email and retrieve the chat history
        user_document = user_reference.document(email)
        chat_history = user_document.get().to_dict().get('chat_history', [])

        # Delete the message from the chat history
        new_chat_history = [
            record for record in chat_history
            if record.get('user_message') != delete_message
        ]

        # Check if the message was found and deleted
        if len(new_chat_history) == len(chat_history):
            return jsonify({'error': 'Message not found in chat history.'}), 404

        # Save the updated chat history to the database after deleting the message
        user_document.update({'chat_history': new_chat_history})
        return jsonify({'message': 'Message deleted successfully.'})
    except Exception as exc:
        runtime_error('delete_message', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500
