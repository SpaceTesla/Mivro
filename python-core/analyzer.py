import os
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key="")

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the safety settings
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

with open('analyzer_instructions.md', 'r') as file:
    system_instructions = file.read()

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=system_instructions
   
)


def calculate_bmi(weight, height):
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)
    return round(bmi, 2)

age = int(input("Enter your age: "))
gender = input("Enter your gender: ")
weight = float(input("Enter your weight (in kg): "))
height = float(input("Enter your height (in cm): "))
bmi = calculate_bmi(weight, height)
dietary_preferences = input("Enter your dietary preferences: ")
medical_conditions = input("Enter your medical conditions: ")
allergies = input("Enter your allergies: ")

# Start a chat session
chat_session = model.start_chat(
    history=[]
)

# Prepare the input string
input_string = f"""Food Product: Amul Chocolate Brownie
Age: {age}
Gender: {gender}
Weight: {weight} kg
Height: {height} cm
BMI: {bmi}
Dietary Preferences: {dietary_preferences}
Medical Conditions: {medical_conditions}
Allergies: {allergies}
"""

with open ("sample.txt",'r') as file:
    data=file.read()

input_string+=data    

# Send the input to the model
response = chat_session.send_message(input_string)

# Print the response from the model
print(response.text)
