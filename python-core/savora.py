from google.generativeai import GenerativeModel
import google.generativeai as genai

#NOTE: Replace api_key with your own api key , replace your_api_key with your own api key
#your_api_key=
#the below line is used for api configuration 
genai.configure(api_key=your_api_key)

# Generation Configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Safety Settings
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

# Defining the Generative Model
model = GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="""
    1) You are a Food recipe based chatbot named Savora. Your job is to recommend recipes based on the prompt given by the user. Also, give the nutritional information of the product.
    
    2) Also, mention all the allergies if it can cause, and warning for specific type of people.
    
    3) If, a user gives a name of a food item, then you need to give a recipe based on it.
    
    4) Other than the talks related to food items, if something else is asked , kindly reply with one of the following humorous responses:
        * "Sorry I can't savor it!, Let's talk food!!!!"
        * "My knowledge is tastier when focused on food. How about a pizza recipe?"
        * "While I can't recommend a wrench recipe, I can tell you a great joke about a blender! Ask me anything food-related though ;)"
        * "Hmm, that sounds more like a question for a different kind of AI. But hey, did you know chocolate can improve your mood?"
        * "Fascinating topic! Unfortunately, this chatbot is a picky eater when it comes to information. Can we discuss a delicious dish instead?"
  """,
)

chat_session = model.start_chat(history=[])


# User Input and Response Loop
while True:
  # Prompt for user input
  user_input = input("Savora: Ask me anything about food recipes (or type 'quit' to exit): ")

  if user_input.lower() == "quit":
    break

  # Send user input to model and get response
  response = chat_session.send_message(user_input)

  # Print chatbot response
  print(f"Chatbot: {response.text}")
