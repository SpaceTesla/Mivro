# Core library imports: Firebase Admin SDK setup
from firebase_admin import auth, firestore
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions and models
from database import user_reference, validate_user_profile, save_health_profile
from models import HealthProfile, FavoriteProduct

# Blueprint for the user routes
user_blueprint = Blueprint('user', __name__, url_prefix='/api/v1/user')

@user_blueprint.route('/load-profile', methods=['POST'])
def load_profile() -> Response:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and retrieve the user profile data
        user_document = user_reference.document(email)
        return jsonify(user_document.get().to_dict())
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/update-user-profile', methods=['POST'])
def update_user_profile() -> Response:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and update the profile fields
        user_document = user_reference.document(email)
        update_data = {}

        if (display_name := request.json.get('display_name')) not in [None, '']:
            update_data['account_info.display_name'] = display_name
        if (photo_url := request.json.get('photo_url')) not in [None, '']:
            update_data['account_info.photo_url'] = photo_url
        if (phone_number := request.json.get('phone_number')) not in [None, '']:
            update_data['account_info.phone_number'] = phone_number

        # Update the user document with the new user profile data
        if update_data:
            user_document.update(update_data)
            return jsonify({'message': 'User profile updated successfully.'})
        else:
            return jsonify({'message': 'No changes detected.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/submit-health-profile', methods=['POST'])
def submit_health_profile() -> Response:
    # Get email from the incoming JSON request
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Check if the user exists in Firebase Auth
        if not auth.get_user_by_email(email):
            return jsonify({'error': 'User not found.'}), 404

        # Create an instance of HealthProfile using the request data
        health_data = HealthProfile(
            age=request.json.get('age'),
            gender=request.json.get('gender'),
            height=request.json.get('height'),
            weight=request.json.get('weight'),
            dietary_preferences=request.json.get('dietary_preferences'),
            allergies=request.json.get('allergies'),
            medical_conditions=request.json.get('medical_conditions')
        )

        # Store the health profile data for the user in Firestore
        result = save_health_profile(email, health_data.to_dict())
        if 'error' in result:
            return jsonify(result), 500

        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/update-health-profile', methods=['POST'])
def update_health_profile() -> Response:
    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and update the health profile fields
        user_document = user_reference.document(email)
        update_data = {}

        if (age := request.json.get('age')) not in [None, '']:
            update_data['health_profile.age'] = age
        if (gender := request.json.get('gender')) not in [None, '']:
            update_data['health_profile.gender'] = gender
        if (height := request.json.get('height')) not in [None, '']:
            update_data['health_profile.height'] = height
        if (weight := request.json.get('weight')) not in [None, '']:
            update_data['health_profile.weight'] = weight
        if (dietary_preferences := request.json.get('dietary_preferences')) not in [None, '']:
            update_data['health_profile.dietary_preferences'] = dietary_preferences
        if (allergies := request.json.get('allergies')) not in [None, '']:
            update_data['health_profile.allergies'] = allergies
        if (medical_conditions := request.json.get('medical_conditions')) not in [None, '']:
            update_data['health_profile.medical_conditions'] = medical_conditions

        # Update the user document with the new health profile data
        if update_data:
            user_document.update(update_data)
            return jsonify({'message': 'Health profile updated successfully.'})
        else:
            return jsonify({'message': 'No changes detected.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/add-favorite', methods=['POST'])
def add_favorite() -> Response:
    # Get email, product name, brand, and image values from the incoming JSON data
    email = request.json.get('email')
    product_name = request.json.get('product_name')
    product_brand = request.json.get('product_brand')
    product_image = request.json.get('product_image')

    if not email or not product_name or not product_brand or not product_image:
        return jsonify({'error': 'Email, product name, brand, and image are required.'}), 400

    try:
        # Reference the user document by email and add the favorite product
        user_document = user_reference.document(email)
        if not user_document.get().exists:
            return jsonify({'error': 'User not found.'}), 404

        # Store the favorite product data for the user in Firestore
        favorite_product = FavoriteProduct(product_name=product_name, product_brand=product_brand, product_image=product_image)
        user_document.set({
            'favorite_product': firestore.ArrayUnion([favorite_product.to_dict()])
        }, merge=True) # Merge the favorite product with the existing user document (if any)

        return jsonify({'message': 'Favorite product added successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/clear-scan-history', methods=['POST'])
@user_blueprint.route('/clear-search-history', methods=['POST'])
@user_blueprint.route('/clear-chat-history', methods=['POST'])
@user_blueprint.route('/clear-favorite-product', methods=['POST'])
def clear_history() -> Response:
    # Mapping of the request path to the Firestore document field to clear
    path_mapping = {
        '/api/v1/user/clear-scan-history': 'scan_history',
        '/api/v1/user/clear-search-history': 'search_history',
        '/api/v1/user/clear-chat-history': 'chat_history',
        '/api/v1/user/clear-favorite-product': 'favorite_product'
    }

    # Get email and password values from the incoming JSON data
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    try:
        # Validate the user's email and password
        result = validate_user_profile(email, password)
        if 'error' in result:
            return jsonify(result), 401

        # Reference the user document by email and clear the specified field
        user_document = user_reference.document(email)
        user_document.update({path_mapping.get(request.path): firestore.DELETE_FIELD})

        return jsonify({'message': f'{path_mapping.get(request.path).replace("_", " ").capitalize()} cleared successfully.'})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
