def additive_name(additives_tags, additives_data):
    return [
        additives_data.get(additive, 'Unknown')
        for additive in additives_tags
    ]

def nova_name(nova_group):
    group_names = {
        1: 'Unprocessed or minimally processed foods',
        2: 'Processed culinary ingredients',
        3: 'Processed foods',
        4: 'Ultra-processed food and drink products'
    }
    return group_names.get(nova_group, 'Unknown')

def grade_color(nutriscore_grade):
    grade_colors = {
        'a': 'green',
        'b': 'blue',
        'c': 'yellow',
        'd': 'orange',
        'e': 'red'
    }
    return grade_colors.get(nutriscore_grade.lower(), 'gray')

def score_assessment(nutriscore_score):
    if nutriscore_score >= 90:
        return 'excellent'
    elif nutriscore_score >= 70:
        return 'good'
    elif nutriscore_score >= 50:
        return 'average'
    elif nutriscore_score >= 30:
        return 'poor'
    else:
        return 'very poor'
