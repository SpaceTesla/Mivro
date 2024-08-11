# Core library imports: Open Food Facts API setup
import openfoodfacts
import json
import sys
from flask import Blueprint, request, jsonify
from datetime import datetime

# Local project-specific imports: Mapping, utilities, database, and gemini functions
from mapping import additive_name, nova_name, grade_color, score_assessment
from utils import filter_additive, filter_ingredient, filter_nutriment, filter_image, filter_data
from database import database_history, database_search
from gemini import lumi, swapr

# Blueprint for the search routes
search_blueprint = Blueprint('search', __name__, url_prefix='/api/v1/search')
api = openfoodfacts.API(user_agent='Mivro/2.9.8') # Initialize the Open Food Facts API client

@search_blueprint.route('/barcode', methods=['POST'])
def barcode() -> dict:
    try:
        # Start the timer for measuring the response time
        start_time = datetime.now()
        # Get the email and product barcode values from the incoming JSON data
        email = request.json.get('email')
        product_barcode = request.json.get('product_barcode')

        if not email or not product_barcode:
            return jsonify({'error': 'Email and product barcode are required.'}), 400

        # Define product schema fields and fetch data from Open Food Facts API using barcode
        required_data = json.load(open('metadata/product_schema.json'))
        product_data = api.product.get(product_barcode, fields=required_data)
        if not product_data:
            return jsonify({'error': 'Product not found.'}), 404

        # Check for missing fields in the product data
        missing_fields = set(required_data) - set(product_data.keys())
        for field in missing_fields:
            print(f'Warning: Data for "{field}" is missing.')

        # Filter the additive numbers, nutriments, and clean the product data
        product_data['additives_tags'] = filter_additive(product_data.get('additives_tags', []))
        filtered_product_data = filter_data(product_data)
        filtered_product_data['nutriments'] = filter_nutriment(filtered_product_data.get('nutriments', {}))

        # Calculate the response time and size for the filtered product data
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        response_size = sys.getsizeof(filtered_product_data) / 1024

        # Update the filtered product data with additional information
        filtered_product_data.update({
            'search_type': 'Open Food Facts API',
            'search_response': '200 OK',
            'response_time': f'{response_time:.2f} seconds',
            'response_size': f'{response_size:.2f} KB',
            'search_date': datetime.now().strftime('%d-%B-%Y'),
            'search_time': datetime.now().strftime('%I:%M %p'),
            'additives_names': additive_name(filtered_product_data.get('additives_tags', []),
                                             json.load(open('metadata/additive_names.json'))),
            'ingredients': filter_ingredient(filtered_product_data.get('ingredients', [])),
            'nova_group_name': nova_name(filtered_product_data.get('nova_group', '')),
            'nutriments': lumi(filtered_product_data.get('nutriments', {})),
            'nutriscore_grade_color': grade_color(filtered_product_data.get('nutriscore_grade', '')),
            'nutriscore_assessment': score_assessment(filtered_product_data.get('nutriscore_score', None)).title(),
            'health_risk': lumi(filtered_product_data.get('ingredients', [])),
            'selected_images': filter_image(filtered_product_data.get('selected_images', [])),
            'recommeded_product': swapr(email, filtered_product_data)
        })

        # Store the scan history for the product barcode in Firestore
        database_history(email, product_barcode, filtered_product_data)
        return jsonify(filtered_product_data)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500

# @search_blueprint.route('/text', methods=['POST'])
# def text() -> dict:
#     try:
#         email = request.form.get('email')
#         product_name = request.form.get('product_name')
#         if not product_name:
#             return jsonify({'error': 'Email and product name are required.'}), 400

#         product_data = api.product.text_search(product_name)
#         if not product_data:
#             return jsonify({'error': 'Product not found.'}), 404

#         return jsonify(product_data)
#     except Exception as exc:
#         return jsonify({'error': str(exc)}), 500

@search_blueprint.route('/database', methods=['POST'])
def database() -> dict:
    try:
        # Start the timer for measuring the response time
        start_time = datetime.now()
        # Get the email and product keyword values from the incoming JSON data
        email = request.json.get('email')
        product_keyword = request.json.get('product_keyword')

        if not email or not product_keyword:
            return jsonify({'error': 'Email and product keyword are required.'}), 400

        search_keys = ['_keywords', 'brands', 'categories', 'product_name'] # Define the search keys for the database search

        # Split the product keyword into individual words and search the database for each word
        tokenized_keywords = product_keyword.split()
        for keyword in tokenized_keywords:
            product_data = database_search(email, keyword, search_keys)
            # Check if the product data is found in the database and return the response
            if product_data:
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                response_size = sys.getsizeof(product_data) / 1024

                product_data.update({
                    'search_type': 'Google Firestore Database',
                    'search_response': '200 OK',
                    'response_time': f'{response_time:.2f} seconds',
                    'response_size': f'{response_size:.2f} KB',
                    'search_date': datetime.now().strftime('%d-%B-%Y'),
                    'search_time': datetime.now().strftime('%I:%M %p')
                })

                return jsonify(product_data)

        return jsonify({'error': 'Product not found.'}), 404
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
