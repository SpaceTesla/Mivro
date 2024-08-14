# Core library imports: Flask setup
from flask import Flask
from flask_cors import CORS

# Local project-specific imports: Configuration, blueprints, and middleware
from config import FLASK_SECRET_KEY
from auth import auth_blueprint
from search import search_blueprint
from gemini import ai_blueprint
from user import user_blueprint
from chat import chat_blueprint
from middleware import authenticate

app = Flask(__name__) # Initialize Flask application instance
app.secret_key = FLASK_SECRET_KEY # Set the Flask secret key for session management

# Register blueprints for API routes
app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(search_blueprint, url_prefix='/api/v1/search')
app.register_blueprint(ai_blueprint, url_prefix='/api/v1/ai')
app.register_blueprint(user_blueprint, url_prefix='/api/v1/user')
app.register_blueprint(chat_blueprint, url_prefix='/api/v1/chat')

# Apply the authenticate middleware to all incoming requests
# app.before_request(authenticate) (COMMENTED OUT: Authentication through HTTP headers are exposed in the frontend)
# Enable CORS for all routes under /api/*
CORS(app, resources={
    r'/api/*': {
        'origins': ['*']
    }
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # Run the app on localhost:5000 in debug mode
