# Function for mapping the additive number to a human-readable name (Uses additive_names.json)
def additive_name(additives_tags: list, additives_data: dict) -> list:
    return [
        additives_data.get(additive, 'Unknown')
        for additive in additives_tags
    ]

# Function for mapping the nova group number to a human-readable name (Used in search.py)
def nova_name(nova_group: int) -> str:
    group_names = {
        1: 'Unprocessed or minimally processed foods',
        2: 'Processed culinary ingredients',
        3: 'Processed foods',
        4: 'Ultra-processed food and drink products'
    }
    return group_names.get(nova_group, 'Unknown')

# Function for mapping the nutriscore grade to a color code (Used in search.py)
def grade_color(nutriscore_grade: str) -> str:
    grade_colors = {
        'a': '#8AC449',
        'b': '#8FD0FF',
        'c': '#FFD65A',
        'd': '#F8A72C',
        'e': '#DF5656'
    }
    return grade_colors.get(nutriscore_grade.lower(), 'gray')

# Function for mapping the nutriscore score to an assessment category (Used in search.py)
def score_assessment(nutriscore_score) -> str:
    if nutriscore_score is None:
        return 'Unknown'
    elif nutriscore_score >= 90:
        return 'excellent'
    elif nutriscore_score >= 70:
        return 'good'
    elif nutriscore_score >= 50:
        return 'average'
    elif nutriscore_score >= 30:
        return 'poor'
    else:
        return 'very poor'

# Function for getting the icon based on the category map (Used in utils.py)
def food_icon(name: str, category_map: dict) -> str:
    for category, items in category_map.items():
        if name in items:
            return category.lower().replace(' ', '-')
    return name.lower().replace(' ', '-')
