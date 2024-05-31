import re
from database import user_reference

def filter_additive(additive_data):
    additive_info = [
        tag
        for tag in additive_data
        if not tag.endswith('i')
    ]
    return additive_info

def filter_ingredient(ingredient_data):
    ingredient_info = [
        {
            'name': ingredient.get('text', '').title(),
            'percentage': f"{abs(float(ingredient.get('percent_estimate', 0))):.2f} %"
        }
        for ingredient in ingredient_data
        if ingredient.get('text') and ingredient.get('percent_estimate', 0) != 0
    ]
    return ingredient_info

def analyse_nutrient(nutrient_data, nutrient_limits):
    positive_nutrients = {}
    negative_nutrients = {}

    nutrient_items = {
        nutrient: {
            'name': nutrient.title(),
            'quantity': f"{abs(float(nutrient_data.get(f'{nutrient}_100g', 0))):.2f} {value['unit']}"
        }
        for nutrient, value in nutrient_limits.items()
        if nutrient_data.get(f'{nutrient}_100g', 0) != 0
    }

    for nutrient, value in nutrient_items.items():
        lower_limit = nutrient_limits[nutrient]['lower_limit']
        upper_limit = nutrient_limits[nutrient]['upper_limit']

        if float(value['quantity'].split()[0]) < lower_limit or float(value['quantity'].split()[0]) > upper_limit:
            negative_nutrients[nutrient] = value
        else:
            positive_nutrients[nutrient] = value

    nutriment_info = {
        'positive_nutrient': list(positive_nutrients.values()),
        'negative_nutrient': list(negative_nutrients.values())
    }
    return nutriment_info

def filter_image(image_data):
    image_link = next(
        iter(
            list(image_data.values())[0].values()
        ), None
    )
    return image_link

def filter_data(product_data):
    product_info = {
        key: [
            re.sub(r'^en:', '', item) if isinstance(item, str) else item
            for item in value
        ]
        if isinstance(value, list) else re.sub(r'^en:', '', value)
        if isinstance(value, str) else value
        for key, value in product_data.items()
    }
    return product_info

def user_profile(email):
    user_document = user_reference.document(email)
    health_profile = user_document.get().to_dict().get('health_profile', {})
    return health_profile

def chat_history(email, chat_entry):
    user_document = user_reference.document(email)
    chat_history = user_document.get().to_dict().get('chat_history', [])

    chat_history.append(chat_entry.to_dict())
    user_document.set({
        'chat_history': chat_history
    }, merge=True)

def calculate_bmi(weight_kg, height_m):
    return round(weight_kg / (height_m ** 2), 2)
