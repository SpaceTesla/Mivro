import google.generativeai as genai

# Configure the API key
genai.configure(api_key="")

# Configuration for the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings for the model
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]


with open('recommend_instructions.md', 'r') as file:
    system_instructions = file.read()

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=system_instructions
   
)
# Start a chat session
chat_session = model.start_chat(history=[])

# Take input from the terminal
user_input = input("Please enter the food item and JSON data: ")


with open ("food_example.json",'r') as file:
    data=file.read()

user_input+=data
# Send the user input to the model and get the response
response = chat_session.send_message(user_input)

# Print the response from the model
print(response.text)

