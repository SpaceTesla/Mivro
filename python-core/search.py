import openfoodfacts
import json
import re
import sys
from flask import Blueprint, request, jsonify
from datetime import datetime

from mapping import additive_name, group_name, grade_color, score_color
from utils import filter_additive, filter_ingredient, analyse_nutrient, filter_image
from database import database_history, database_search

search_blueprint = Blueprint('search', __name__, url_prefix='/api/v1/search')
api = openfoodfacts.API(user_agent='Mivro/2.4')

@search_blueprint.route('/barcode', methods=['POST'])
def barcode():
    start_time = datetime.now()
    email = request.json.get('email')
    product_barcode = request.json.get('product_barcode')
    required_data = json.load(open('product_schema.json'))

    product_data = api.product.get(product_barcode, fields=required_data)
    if not product_data:
        return jsonify({'error': 'Product not found.'})

    missing_fields = set(required_data) - set(product_data.keys())
    for field in missing_fields:
        print(f'Warning: Data for "{field}" is missing.')

    product_data['additives_tags'] = filter_additive(product_data['additives_tags'])
    product_data = {
        key: [
            re.sub(r'^en:', '', item) if isinstance(item, str) else item
            for item in value
        ]
        if isinstance(value, list) else re.sub(r'^en:', '', value)
        if isinstance(value, str) else value
        for key, value in product_data.items()
    }

    end_time = datetime.now()
    response_time = (end_time - start_time).total_seconds()
    response_size = sys.getsizeof(product_data) / 1024

    product_data.update({
        'search_type': 'Open Food Facts API',
        'search_response': '200 OK',
        'response_time': f'{response_time:.2f} seconds',
        'response_size': f'{response_size:.2f} KB',
        'search_date': datetime.now().strftime('%d-%B-%Y'),
        'search_time': datetime.now().strftime('%I:%M %p'),
        'additives_names': additive_name(product_data['additives_tags'], json.load(open('additive_names.json'))),
        'ingredients': filter_ingredient(product_data['ingredients']),
        'nova_group_name': group_name(product_data['nova_group']),
        'nutriments': analyse_nutrient(product_data['nutriments'], json.load(open('nutrient_limits.json'))),
        'nutriscore_grade_color': grade_color(product_data['nutriscore_grade']),
        'nutriscore_score_color': score_color(product_data['nutriscore_score']),
        'selected_images': filter_image(product_data['selected_images'])
    })

    database_history(email, product_barcode, product_data)
    return jsonify(product_data)

# @search_blueprint.route('/text', methods=['POST'])
# def text():
#     product_name = request.form.get('product_name')
#     product_data = api.product.text_search(product_name)

#     if not product_data:
#         return jsonify({'error': 'Product not found.'})

#     return jsonify(product_data)

@search_blueprint.route('/database', methods=['POST'])
def database():
    start_time = datetime.now()
    product_keyword = request.json.get('product_keyword')
    search_keys = ['_keywords', 'brands', 'categories', 'product_name']

    product_data = database_search(product_keyword, search_keys)
    if not product_data:
        return jsonify({'error': 'Product not found.'})

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
