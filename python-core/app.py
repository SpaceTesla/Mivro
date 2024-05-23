from flask import Flask
from flask_cors import CORS

from config import FLASK_SECRET_KEY
from search import search_blueprint
from authentication import auth_blueprint
from gemini import ai_blueprint

app = Flask(__name__)  # Create a Flask application instance
app.secret_key = FLASK_SECRET_KEY  # Set the Flask secret key for session management
app.register_blueprint(search_blueprint)  # Register the search blueprint
app.register_blueprint(auth_blueprint)  # Register the auth blueprint
app.register_blueprint(ai_blueprint)  # Register the ai blueprint

# Enable CORS for all routes under /api/*, allowing all origins
CORS(app, resources={
    r'/api/*': {
        'origins': ['*']
    }
})

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
