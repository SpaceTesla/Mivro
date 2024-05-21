import google.generativeai as genai
from google.generativeai import GenerativeModel
from flask import Blueprint, request, jsonify
from config import GEMINI_API_KEY

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
    user_message = request.json.get('message')
    bot_response = chat_session.send_message(user_message)
    return jsonify({'response': bot_response.text})
