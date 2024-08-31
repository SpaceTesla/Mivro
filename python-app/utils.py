# Core library imports: Regular expressions and JSON parsing
import json
import re

# Local project-specific imports: Mapping and database functions
from mapping import food_icon
from database import user_reference

# with open('metadata/nutrient_limits.json') as file:
#     nutrient_limits = json.load(file)

with open('metadata/food_categories.json') as file:
    food_categories = json.load(file)

# Function for filtering additive tags and removing the 'i' suffix (Used in search.py)
def filter_additive(additive_data: list) -> list:
    additive_info = [
        tag
        for tag in additive_data
        if not tag.endswith('i')
    ]
    return additive_info

# Function for filtering ingredient data and extracting the name, icon, and percentage (Used in search.py)
def filter_ingredient(ingredient_data: list) -> list:
    ingredient_info = [
        {
            'name': ingredient.get('text', '').title(),
            'icon': food_icon(ingredient.get('text', '').title(), food_categories),
            'percentage': f"{abs(float(ingredient.get('percent_estimate', 0))):.2f} %"
        }
        for ingredient in ingredient_data
        if ingredient.get('text') and ingredient.get('percent_estimate', 0) != 0
    ]
    return ingredient_info

# Function for mapping the nutrient name to an icon (Used in search.py)
def filter_nutriment(nutriment_data: dict) -> dict:
    for category in ['negative_nutrient', 'positive_nutrient']:
        if category in nutriment_data:
            for nutrient in nutriment_data[category]:
                nutrient['icon'] = food_icon(nutrient.get('name', ''), food_categories)
    return nutriment_data

# DEPRECATED: Replaced by Gemini model for the same purpose
# Function for analysing the nutrient data based on the nutrient limits (Used in search.py)
def analyse_nutrient(nutrient_data: dict, nutrient_limits: dict) -> dict:
    positive_nutrients = {}
    negative_nutrients = {}

    nutrient_map = {
        nutrient: {
            'name': nutrient.title(),
            'icon': food_icon(nutrient.title(), food_categories),
            'quantity': f"{abs(float(nutrient_data.get(f'{nutrient}_100g', 0))):.2f} {value['unit']}"
        }
        for nutrient, value in nutrient_limits.items()
        if nutrient_data.get(f'{nutrient}_100g', 0) != 0
    }

    # Check if the nutrient quantity is within the recommended limits
    for nutrient, value in nutrient_map.items():
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

# Function for filtering the product data and removing the 'en:' prefix (Used in search.py)
def filter_data(product_data: dict) -> dict:
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

# Function for filtering the image data and extracting the image link (Used in search.py)
def filter_image(image_data: dict) -> str:
    image_link = next(
        iter(
            list(image_data.values())[0].values() # Return the first image link from the data
        ), None
    )
    return image_link

# Function for retrieving the user's health profile from Firestore (Used in gemini.py)
def health_profile(email: str) -> dict:
    user_document = user_reference.document(email)
    health_profile = user_document.get().to_dict().get('health_profile', {})
    return health_profile

# Function for storing the chat history in Firestore (Used in gemini.py)
def chat_history(email: str, chat_entry: dict) -> None:
    user_document = user_reference.document(email)
    if not user_document.get().exists:
        user_document.set({ 'chat_history': [] })

    chat_history = user_document.get().to_dict().get('chat_history', [])
    chat_history.append(chat_entry.to_dict())
    user_document.set({
        'chat_history': chat_history
    }, merge=True)

# Function for calculating the BMI based on the weight and height (Used in models.py)
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if not weight_kg or not height_m:
        return None

    return round(weight_kg / (height_m ** 2), 2)
