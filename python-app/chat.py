# Core library imports: Flask setup
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions
from database import user_reference

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

        # Use list comprehension to update the message
        new_chat_history = [
            {**record, 'user_message': new_message} if record.get('user_message') == old_message else record
            for record in chat_history
        ]

        # Check if the old message was found and updated
        if new_chat_history == chat_history:
            return jsonify({'error': 'Old message not found in chat history.'}), 404

        # Update the chat history in the database
        user_document.update({'chat_history': new_chat_history})
        return jsonify({'message': 'Message updated successfully.'})
    except Exception as exc:
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

        # Use list comprehension to delete the message
        new_chat_history = [
            record for record in chat_history
            if record.get('user_message') != delete_message
        ]

        # Check if the message was found and deleted
        if len(new_chat_history) == len(chat_history):
            return jsonify({'error': 'Message not found in chat history.'}), 404

        # Update the chat history in the database
        user_document.update({'chat_history': new_chat_history})
        return jsonify({'message': 'Message deleted successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
