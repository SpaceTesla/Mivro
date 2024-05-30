import requests
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

with open('lumi_instructions.md', 'r') as file:
    lumi_instructions = file.read()

with open('swapr_instructions.md', 'r') as file:
    swapr_instructions = file.read()

with open('savora_instructions.md', 'r') as file:
    savora_instructions = file.read()

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

lumi_chat_session = lumi_llm.start_chat(history=[])
swapr_chat_session = swapr_llm.start_chat(history=[])
savora_chat_session = savora_llm.start_chat(history=[])

@ai_blueprint.route('/lumi', methods=['POST'])
def lumi(product_data):
    email = request.json.get('email')
    health_profile = user_profile(email)

    user_message = f'Health Profile: {health_profile}\nProduct Data: {product_data}'
    bot_response = lumi_chat_session.send_message(user_message)

    filtered_response = bot_response.text.replace('```python', '').replace('```', '')
    return eval(filtered_response)

def user_profile(email):
    user_document = user_reference.document(email)
    health_profile = user_document.get().to_dict().get('health_profile', {})
    return health_profile

@ai_blueprint.route('/swapr', methods=['POST'])
def swapr(email, product_data):
    user_message = f'Product Data: {product_data}'
    bot_response = swapr_chat_session.send_message(user_message)
    database_response = requests.post(
        'http://localhost:5000/api/v1/search/database',
        json={'email': email, 'product_keyword': bot_response.text}
    )
    return database_response.json()

@ai_blueprint.route('/savora', methods=['POST'])
def savora():
    email = request.json.get('email')
    user_message = request.json.get('message')
    bot_response = savora_chat_session.send_message(user_message)

    chat_entry = ChatHistory(user_message=user_message, bot_response=bot_response.text)
    chat_history(email, chat_entry)
    return jsonify({'response': bot_response.text})

def chat_history(email, chat_entry):
    user_document = user_reference.document(email)
    chat_history = user_document.get().to_dict().get('chat_history', [])

    chat_history.append(chat_entry.to_dict())
    user_document.set({
        'chat_history': chat_history
    }, merge=True)
