# Core library imports: Google Generative AI setup
import requests
import google.generativeai as genai
from google.generativeai import GenerativeModel
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Configuration, models, and utilities
from config import GEMINI_API_KEY
from models import ChatHistory
from utils import user_profile, chat_history

# Blueprint for the ai routes
ai_blueprint = Blueprint('ai', __name__, url_prefix='/api/v1/ai')
genai.configure(api_key=GEMINI_API_KEY) # Load Gemini API key from .env

# Generation settings to control the model's output
generation_config = {
    'temperature': 1,
    'top_p': 0.95,
    'top_k': 64,
    'max_output_tokens': 8192,
    'response_mime_type': 'text/plain'
}

# Safety settings to block harmful content (BLOCK_NONE is set to ignore triggers in product data for accurate context processing)
# Thresholds: BLOCK_NONE, BLOCK_LOW_AND_ABOVE, BLOCK_MEDIUM_AND_ABOVE, BLOCK_ONLY_HIGH
safety_settings = [
    {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
    {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
    {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
    {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'}
]

# Load system instructions for the Gemini model
with open('instructions/lumi_instructions.md', 'r') as file:
    lumi_instructions = file.read()

with open('instructions/swapr_instructions.md', 'r') as file:
    swapr_instructions = file.read()

with open('instructions/savora_instructions.md', 'r') as file:
    savora_instructions = file.read()

# Initialize the Gemini model with custom settings and instructions
lumi_llm = GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=lumi_instructions
)

swapr_llm = GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=swapr_instructions
)

savora_llm = GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=savora_instructions
)

# Start a chat session with the Gemini model
lumi_chat_session = lumi_llm.start_chat(history=[])
swapr_chat_session = swapr_llm.start_chat(history=[])
savora_chat_session = savora_llm.start_chat(history=[])

@ai_blueprint.route('/lumi', methods=['POST'])
def lumi(product_data: dict) -> Response:
    try:
        # Get the user's health profile based on their email
        email = request.json.get('email')
        if not email or not product_data:
            return jsonify({'error': 'Email and product data are required.'}), 400

        health_profile = user_profile(email) # Retrieve the user's health profile from Firestore (if any)
        # Send the user's health profile and product data to the Gemini model
        user_message = f'Health Profile: {health_profile}\nProduct Data: {product_data}'
        bot_response = lumi_chat_session.send_message(user_message)

        # Filter the response to remove code blocks and return the evaluated product data
        filtered_response = bot_response.text.replace('```python', '').replace('```', '')
        return eval(filtered_response) # If eval() throws an error, use ast.literal_eval() or json.loads() instead
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@ai_blueprint.route('/swapr', methods=['POST'])
def swapr(email: str, product_data: dict) -> Response:
    try:
        # Send the product data to the Gemini model
        user_message = f'Product Data: {product_data}'
        bot_response = swapr_chat_session.send_message(user_message)

        # Filter the response to remove bold formatting and search the database for the product name
        filtered_response = bot_response.text.replace('**', '')
        database_response = requests.post(
            'http://localhost:5000/api/v1/search/database',
            json={'email': email, 'product_keyword': filtered_response}
        )

        if database_response.status_code != 200:
            # return jsonify({'error': 'Database search failed.'}), database_response.status_code
            return {'product_name': filtered_response}

        return database_response.json()
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@ai_blueprint.route('/savora', methods=['POST'])
def savora() -> Response:
    try:
        # Get the user's email and message to send to the Gemini model
        email = request.json.get('email')
        user_message = request.json.get('message')
        if not email or not user_message:
            return jsonify({'error': 'Email and message are required.'}), 400

        bot_response = savora_chat_session.send_message(user_message)
        # Store the chat history for the user's email in Firestore
        chat_entry = ChatHistory(user_message=user_message, bot_response=bot_response.text)
        chat_history(email, chat_entry)

        return jsonify({'response': bot_response.text})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
