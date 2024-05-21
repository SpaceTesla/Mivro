### Food Product Analysis Prompt

Given a food product name and a dictionary containing all its nutrients and possible allergens, we aim to analyze them based on the following criteria:

- **Age**
- **Gender**
- **Weight**
- **Height**
- **BMI** (calculated internally)
- **Dietary Preferences**
- **Medical Conditions**
- **Allergies**

#### Dietary Preferences

Choose one from the following:

1. None
2. Gluten-Free
3. Halal
4. High Protein
5. Keto
6. Kosher
7. Lactose-Free
8. Low Carb
9. Low Fat
10. Nut-Free
11. Organic
12. Paleo
13. Pescatarian
14. Vegan
15. Vegetarian

#### Medical Conditions

Select any applicable conditions:

1. None
2. Anemia
3. Asthma
4. Celiac Disease
5. Diabetes
6. GERD
7. Heart Disease
8. High Cholesterol
9. Hypertension
10. IBS
11. Lactose Intolerance
12. Obesity
13. PCOS
14. Pregnant
15. Thyroid Disorder

#### Allergies

Choose any allergens:

1. None
2. Corn
3. Dairy
4. Eggs
5. Fish
6. Gluten
7. Lupin
8. Mustard
9. Peanuts
10. Sesame
11. Shellfish
12. Soy
13. Sulfites
14. Tree Nuts
15. Wheat

Analyze the nutrients, categorizing them into positive and negative based on the personalized data provided and the standard guidelines worldwide. Additionally, provide warnings for allergens. Return this information as a dictionary with three keys: `positive_nutrients`, `negative_nutrients`, and `warnings`.

The `positive_nutrients` and `negative_nutrients` should also include the quantity.

Provide the output in the form of a Python dictionary.No further explanation is needed, just return the dictonary.
