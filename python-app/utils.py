import re
from database import user_reference

# Function for filtering additive tags and removing the 'i' suffix (Used in search.py)
def filter_additive(additive_data: list) -> list:
    additive_info = [
        tag
        for tag in additive_data
        if not tag.endswith('i')
    ]
    return additive_info

# Function for filtering ingredient data and extracting the name and percentage (Used in search.py)
def filter_ingredient(ingredient_data: list) -> list:
    ingredient_info = [
        {
            'name': ingredient.get('text', '').title(),
            'percentage': f"{abs(float(ingredient.get('percent_estimate', 0))):.2f} %"
        }
        for ingredient in ingredient_data
        if ingredient.get('text') and ingredient.get('percent_estimate', 0) != 0
    ]
    return ingredient_info

# DEPRECATED: Replaced by Gemini model for the same purpose
# Function for analysing the nutrient data based on the nutrient limits (Used in search.py)
def analyse_nutrient(nutrient_data: dict, nutrient_limits: dict) -> dict:
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

    # Check if the nutrient quantity is within the recommended limits
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

# Function for filtering the image data and extracting the image link (Used in search.py)
def filter_image(image_data: dict) -> str:
    image_link = next(
        iter(
            list(image_data.values())[0].values() # Return the first image link from the data
        ), None
    )
    return image_link

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

# Function for retrieving the user's health profile from Firestore (Used in gemini.py)
def user_profile(email: str) -> dict:
    user_document = user_reference.document(email)
    health_profile = user_document.get().to_dict().get('health_profile', {})
    return health_profile

# Function for storing the chat history in Firestore (Used in gemini.py)
def chat_history(email: str, chat_entry: dict) -> None:
    user_document = user_reference.document(email)
    chat_history = user_document.get().to_dict().get('chat_history', [])

    chat_history.append(chat_entry.to_dict())
    user_document.set({
        'chat_history': chat_history
    }, merge=True)

# Function for calculating the BMI based on the weight and height (Used in models.py)
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    return round(weight_kg / (height_m ** 2), 2)
