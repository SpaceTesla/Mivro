import openfoodfacts
import json
from datetime import datetime

def barcode(barcode='8901719104046'):
    api = openfoodfacts.API(user_agent='Green-Elixir/0.3')
    required_data = json.load(open('product_schema.json'))
    product_data = api.product.get(barcode, fields=required_data)

    if not product_data:
        print('Error: Product not found.')
        return

    missing_fields = set(required_data) - set(product_data.keys())
    for field in missing_fields:
        print(f'Warning: Data for "{field}" is missing.')

    ingredient_info = [
        {
            'name': ingredient.get('text', '').title(),
            'percentage': f"{abs(float(ingredient.get('percent_estimate', 0))):.2f} %"
        }
        for ingredient in product_data.get('ingredients', [])
        if ingredient.get('text') and ingredient.get('percent_estimate', 0) != 0
    ]

    essential_nutrients = [
        'calcium', 'carbohydrates', 'cholesterol', 'copper', 'energy-kcal', 'fat', 'fiber', 'iodine', 'iron', 'magnesium',
        'manganese', 'phosphorus', 'potassium', 'proteins', 'saturated-fat', 'selenium', 'sodium', 'sugars', 'zinc'
    ]
    nutriments_info = [
        {
            'name': key.title(),
            'value': f"{float(product_data['nutriments'].get(f'{key}_100g', 0)):.2f} {'kcal' if key == 'energy-kcal' else 'g'}"
        }
        for key in sorted(essential_nutrients)
        if product_data['nutriments'].get(f"{key}_100g") is not None and product_data['nutriments'].get(f"{key}_100g") != 0
    ]

    image_link = next(
        iter(
            next(iter(image_data.values()))
            for image_data in product_data.get('selected_images', {}).values()
        ),
        None
    )

    product_data.update(
        {
            'ingredients': ingredient_info,
            'nutriments': nutriments_info,
            'selected_images': image_link,
            'search_date': datetime.now().strftime('%d-%B-%Y'),
            'search_time': datetime.now().strftime('%I:%M %p')
        }
    )

    formatted_data = json.dumps(product_data, indent=4)
    print(formatted_data)

if __name__ == '__main__':
    barcode()
