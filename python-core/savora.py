import google.generativeai as genai
from google.generativeai import GenerativeModel

genai.configure(api_key='')

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

model = GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_instructions
)

chat_session = model.start_chat(history=[])

while True:
    user_message = input('Savora: ')
    bot_response = chat_session.send_message(user_message)

    print(bot_response.text)
