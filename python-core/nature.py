# Define the recommended daily intake for each nutrient
recommended_intake = {
    'carbohydrates': 300,  # g
    'fat': 70,  # g
    'fiber': 30,  # g
    'proteins': 50,  # g
    'saturated-fat': 20,  # g
    'sugars': 25,  # g
    'calcium': 1000,  # mg
    'cholesterol': 300,  # mg
    'copper': 900,  # µg (example value)
    'iron': 18,  # mg
    'magnesium': 400,  # mg
    'manganese': 2.3,  # mg
    'phosphorus': 700,  # mg
    'potassium': 3500,  # mg
    'sodium': 2300,  # mg
    'zinc': 11,  # mg
    'iodine': 150,  # µg
    'selenium': 55,  # µg
    'water': 2000,  # ml
    'energy-kcal': 2000  # kcal
}

from app import barcode

def process_data():
    barcodes = '8901719104046'  # Example barcode
    product_data = barcode(barcodes)
    
    positives=[]
    negatives=[]
    
    for item in product_data['nutriments']:
        nutri_name=item['name']
        recommend=recommended_intake[nutri_name.lower()]
        
        if float(item['quantity'].split()[0]) > recommend:
            negatives.append(item)
            
        else:
            positives.append(item)
    
    print("The positives are:")
    print(positives)
    print()
    print("The negatives are:")
    print(negatives)
    print()
    
    
    # The NOVA group logic 
    nova_logic={1:"Minimally Processed Food",2:"Processes Culinary Food",3:"Processed Foods",4:"Ultra Processed Food"}
    print("The given food item is rated as:",nova_logic[product_data['nova_group']])
    
    # Nutriscore grade logic
    nutriscore={'a':"Dark Green",'b':'Green','c':"Yellow",'d':"Orange",'e':"Red"}    
    print("The score of the given food is:",product_data['nutriscore_score'])
    print("The grade of the given food is:",nutriscore[product_data['nutriscore_grade']]) 
    
    
    print()
        
    # The nutrient levels 
    print("The nutrient levels of the given data is:")
    for item in product_data['nutrient_levels']:
        print(item,":",product_data['nutrient_levels'][item])
        
        
    print()
    print("The possible allergic items: ")
    for allergic_items in product_data['allergens_tags']:
        print(allergic_items)


if __name__ == '__main__':
    process_data() 
    