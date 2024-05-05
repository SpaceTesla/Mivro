import requests
import datetime 
import json

code = input("Enter the Barcode:")

fields="""code,product_name,keywords,additives_tags,allergens,brands,brands_tags,allergens_from_ingredients,
allergens_hierarchy,allergens_tags,
additives_n,additives_tags,allergens_from_ingredients,categories,
categories_tags,countries,
image_front_small_url,image_front_thumb_url,image_front_url,
image_nutrition_small_url,image_nutrition_thumb_url,
image_nutrition_url,
image_url,image_small_url,image_thumb_url,
ingredients, ingredients_tags,
nutrient_levels,nutrition_grades,
nutrient_levels_tags,nutriments,nutriscore_data,nutriscore_score
quantity,status_verbose
"""

url = "https://world.openfoodfacts.net/api/v2/product/"+code+"?"+'fields='+fields
response = requests.get(url)
data=response.json()

#Adding the date for search history
search_datetime = datetime.datetime.now()
search_date = search_datetime.strftime('%Y-%m-%d') # search  date
search_time = search_datetime.strftime('%H:%M:%S') # search  time

data['search_date'] = search_date
data['search_time'] = search_time

formatted_json = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False) # Used by me to store data in clean format 
print(formatted_json)
