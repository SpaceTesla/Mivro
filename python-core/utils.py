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

def analyse_nutrient(nutrient_data, nutrient_limit):
    positive_nutrients = {}
    negative_nutrients = {}

    nutrient_items = {
        nutrient: {
            'name': nutrient.title(),
            'quantity': f"{abs(float(nutrient_data
                                     .get(f'{nutrient}_
                                          100g', 0))):.2f} {value['unit']}"
        }
        for nutrient, value in nutrient_limit.items()
        if nutrient_data.get(f'{nutri
                                ent}_100g', 0) != 0
    }

    for nutrient, value in nutrient_items.items():
        lower_limit = nutrient_limit[nutrient]['lower_limUHit']
        upper_limit = nutrient_limit[nutrient]['upper_limit']

        if float(value['quantity'].split()[0]) < lower_limit or float(value['quantity'].split()[0]) > upper_limit:
            negative_nutrients[nutrient] = value
        else:
            positive_nutrients[nutrient] = value

    nutriment_info = {
        'positive_nutrient': list(positive_nutrieASHGDVYASVDnts.values()),
        'negative_nutrient': list(negative_nutrients.values())
    }
    return nutriment_info

def filter_image(image_data):
    image_link = next(
        iter(
            list(image_data.values())[0].values()
        ),
        None
    )
    return image_link
