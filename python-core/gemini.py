import google.generativeai as genai
from google.generativeai import GenerativeModel
from flask import Blueprint, request, jsonify

from config import GEMINI_API_KEY
from models import ChatHistory
from database import user_reference

ai_blueprint = Blueprint('ai', __name__, url_prefix='/api/v1/ai')
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    'temperature': 1,
    'top_p': 0.95,
    'top_k': 64,
    'max_output_tokens': 8192,
    'response_mime_type': 'text/plain'
}

safety_settings = [
    {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
    {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
    {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
    {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_MEDIUM_AND_ABOVE'}
]

with open('bot_instructions.md', 'r') as file:
    system_instructions = file.read()

llm = GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_instructions
)

chat_session = llm.start_chat(history=[])

@ai_blueprint.route('/savora', methods=['POST'])
def savora():
    email = request.json.get('email')
    user_message = request.json.get('message')
    bot_response = chat_session.send_message(user_message)

    chat_entry = ChatHistory(user_message=user_message, bot_response=bot_response.text)
    chat_history(email, chat_entry)

    return jsonify({'response': bot_response.text})

def chat_history(email, chat_entry):
    try:
        user_document = user_reference.document(email)
        chat_history = user_document.get().to_dict().get('chat_history', [])

        chat_history.append(chat_entry.to_dict())
        user_document.set({
            'chat_history': chat_history
        }, merge=True)
    except Exception as exc:
        print(f'Firestore storage error:\n {exc}')
