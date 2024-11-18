import re

def find_ingredients_in_string(ingredients, input_string):
    # Normalize the ingredient names
    normalized_ingredients = []
    for ingredient in ingredients:
        name = ingredient['name']
        # Remove any additional descriptors
        name = re.sub(r',.*', '', name)  # Remove anything after a comma
        name = re.sub(r'\b\w+-\w+\b', '', name).strip()  # Remove hyphenated words
        normalized_ingredients.append({'name': name, 'original_name': ingredient['name']})

    found_ingredients = []
    for normalized in normalized_ingredients:
        if normalized['name'].lower() in input_string.lower():
            found_ingredients.append(normalized['name'])

    return found_ingredients



if __name__ == "__main__":
    string = "Mix in remaining 1 1/2 cups flour, remaining 1/2 cup warm water, 2 tablespoons sugar, vegetable oil, and salt."
    ingredients = [
        {'amount': '1 3/4', 'unit': 'cups', 'name': 'all-purpose flour, divided'},
        {'amount': '3/4', 'unit': 'cup', 'name': 'warm water, divided'},
        {'amount': '1', 'unit': 'tablespoon', 'name': 'active dry yeast'},
        {'amount': '1', 'unit': 'teaspoon', 'name': 'white sugar'},
        {'amount': '2', 'unit': 'tablespoons', 'name': 'white sugar'},
        {'amount': '1', 'unit': 'tablespoon', 'name': 'vegetable oil'},
        {'amount': '1/4', 'unit': 'teaspoon', 'name': 'salt'},
        {'amount': '1/2', 'unit': 'teaspoon', 'name': 'baking powder'}
    ]



    found_ingredients = find_ingredients_in_string(ingredients, string)
    print(found_ingredients)
