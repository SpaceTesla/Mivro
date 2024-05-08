import openfoodfacts
import json
from datetime import datetime

def barcode(barcode='8901719104046'):
    api = openfoodfacts.API(user_agent='Green-Elixir/0.4')
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

    nutrient_units = {
        'g': ['carbohydrates', 'fat', 'fiber', 'proteins', 'saturated-fat', 'sugars'],
        'mg': ['calcium', 'cholesterol', 'copper', 'iron', 'magnesium', 'manganese', 'phosphorus', 'potassium', 'sodium', 'zinc'],
        'µg': ['iodine', 'selenium'],
        'ml': ['water'],
        'kcal': ['energy-kcal']
    }
    nutriment_info = [
        {
            'name': nutrient.title(),
            'quantity': f"{float(product_data['nutriments'].get(f'{nutrient}_100g', 0)):.2f} {unit}"
        }
        for unit, nutrients in nutrient_units.items()
        for nutrient in nutrients
        if product_data['nutriments'].get(f'{nutrient}_100g', 0) != 0
    ]

    image_link = next(
        iter(
            list(product_data.get('selected_images', {}).values())[0].values()
        ),
        None
    )

    product_data.update(
        {
            'ingredients': ingredient_info,
            'nutriments': nutriment_info,
            'selected_images': image_link,
            'search_date': datetime.now().strftime('%d-%B-%Y'),
            'search_time': datetime.now().strftime('%I:%M %p')
        }
    )

    formatted_data = json.dumps(product_data, indent=4)
    #print(formatted_data), uncomment it later when you integrate both the codes
    return product_data

if __name__ == '__main__':
    barcode()
