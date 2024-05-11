def additive_name(additives_tag, additives_data):
    return [
        additives_data.get(additive, 'Unknown')
        for additive in additives_tag
    ]

def group_name(nova_group):
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
    # akash was here w=mwahahwhahhwhahwh
    return grade_colors.get(nutriscore_grade.lower(), 'gray')

def score_color(nutriscore_score):
    if nutriscore_score >= 90:
        return 'green'
    elif nutriscore_score >= 70:
        return 'blue'
    elif nutriscore_score >= 50:
        return 'yellow'
    elif nutriscore_score >= 30:
        return 'orange'
    else:
        return 'red'
