import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Access the environment variables
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
