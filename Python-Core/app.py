import openfoodfacts
import json
from datetime import datetime

api = openfoodfacts.API(user_agent='Green-Elixir/0.2')

barcode = '8901719104046'
required_data = json.load(open('product_schema.json'))
product_data = api.product.get(barcode, fields=required_data)

missing_fields = set(required_data) - set(product_data.keys())
for field in missing_fields:
    print(f'Warning: Data for "{field}" is missing.')

product_data.update(
    {
        'search_date': datetime.now().strftime('%d-%B-%Y'),
        'search_time': datetime.now().strftime('%I:%M %p')
    }
)

formatted_data = json.dumps(product_data, indent=4)
print(formatted_data)
