# Core library imports: Firebase Admin SDK setup
from firebase_admin import auth, firestore
from flask import Blueprint, Response, request, jsonify

# Local project-specific imports: Database functions and models
from database import user_reference, flagged_reference, save_health_profile, runtime_error
from models import HealthProfile, FavoriteProduct

# Blueprint for the user routes
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/load-profile', methods=['POST'])
def load_profile() -> Response:
    # Get email value from the request headers
    email = request.headers.get('Mivro-Email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Reference the user document by email and retrieve the user profile data
        user_document = user_reference.document(email)
        return jsonify(user_document.get().to_dict())
    except Exception as exc:
        runtime_error('load_profile', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/update-profile', methods=['POST'])
def update_profile() -> Response:
    # Get email value from the request headers
    email = request.headers.get('Mivro-Email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Reference the user document by email and prepare for updates
        user_document = user_reference.document(email)
        update_data = {}

        # Update account info fields if provided
        if (display_name := request.json.get('display_name')) not in [None, '']:
            update_data['account_info.display_name'] = display_name
        if (photo_url := request.json.get('photo_url')) not in [None, '']:
            update_data['account_info.photo_url'] = photo_url
        if (phone_number := request.json.get('phone_number')) not in [None, '']:
            update_data['account_info.phone_number'] = phone_number

        # Update health profile fields if provided
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

        # Update the user document with the provided data
        if update_data:
            user_document.update(update_data)
            return jsonify({'message': 'Profile updated successfully.'})
        else:
            return jsonify({'message': 'No changes detected.'})
    except Exception as exc:
        runtime_error('update_profile', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/health-profile', methods=['POST'])
def health_profile() -> Response:
    # Get email value from the request headers
    email = request.headers.get('Mivro-Email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    try:
        # Check if the user exists in Firebase Auth
        if not auth.get_user_by_email(email):
            return jsonify({'error': 'User not found.'}), 404

        # Create a HealthProfile object from the incoming JSON data
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
        runtime_error('health_profile', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/favorite-product', methods=['POST'])
def favorite_product() -> Response:
    # Get email, product name, brand, and image values from the incoming JSON data
    email = request.headers.get('Mivro-Email')
    product_name = request.json.get('product_name')
    product_brand = request.json.get('product_brand')
    product_image = request.json.get('product_image')

    if not email or not product_name or not product_brand or not product_image:
        return jsonify({'error': 'Email, product name, brand, and image are required.'}), 400

    try:
        # Reference the user document by email and add the favorite product
        user_document = user_reference.document(email)
        favorite_product = FavoriteProduct(product_name=product_name, product_brand=product_brand, product_image=product_image)
        user_document.set({
            'favorite_products': firestore.ArrayUnion([favorite_product.to_dict()])
        }, merge=True) # Merge the favorite product with the existing user document (if any)

        return jsonify({'message': 'Favorite product added successfully.'})
    except Exception as exc:
        runtime_error('favorite_product', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/flag-product', methods=['POST'])
def flag_product() -> Response:
    # Get email, product name, brand, and description values from the incoming JSON data
    email = request.headers.get('Mivro-Email')
    product_name = request.json.get('product_name')
    product_brand = request.json.get('product_brand')
    flag_reason = request.json.get('description')

    if not email or not product_name or not product_brand or not flag_reason:
        return jsonify({'error': 'Email, product name, brand, and description are required.'}), 400

    try:
        # Reference the user document by email and add the flagged product information
        user_document = flagged_reference.document(email)
        user_document.set({
            'flagged_products': firestore.ArrayUnion([{
                'product_name': product_name,
                'product_brand': product_brand,
                'description': flag_reason
            }])
        }, merge=True) # Merge the flagged product with the existing user document (if any)

        return jsonify({'message': 'Product flagged successfully.'})
    except Exception as exc:
        runtime_error('flag_product', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500

@user_blueprint.route('/clear-scan', methods=['POST'])
@user_blueprint.route('/clear-search', methods=['POST'])
@user_blueprint.route('/clear-chat', methods=['POST'])
@user_blueprint.route('/clear-favorite', methods=['POST'])
def clear_history() -> Response:
    # Get email value from the request headers
    email = request.headers.get('Mivro-Email')
    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    # Map the request path to the corresponding Firestore field to clear
    path_map = {
        '/api/v1/user/clear-scan': 'scan_history',
        '/api/v1/user/clear-search': 'search_history',
        '/api/v1/user/clear-chat': 'chat_history',
        '/api/v1/user/clear-favorite': 'favorite_product'
    }

    try:
        # Reference the user document by email and clear the specified history field
        user_document = user_reference.document(email)
        user_document.update({path_map.get(request.path): firestore.DELETE_FIELD})

        formatted_message = f'{path_map.get(request.path).replace("_", " ").capitalize()}'
        return jsonify({'message': f'{formatted_message} cleared successfully.'})
    except Exception as exc:
        runtime_error('clear_history', str(exc), email=email)
        return jsonify({'error': str(exc)}), 500
