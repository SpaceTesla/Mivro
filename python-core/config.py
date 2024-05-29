import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Access the environment variables
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Set the default name and photo for a user
DEFAULT_NAME = 'Mivro User'
DEFAULT_PHOTO = 'https://i.pinimg.com/736x/5c/06/c9/5c06c94b8588cb6d5f20ff6980a073cd.jpg'
