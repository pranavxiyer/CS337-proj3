def transform_recipe_to_lactose_free(parsed_recipe):
    lactose_free_subs = {
        "milk": "plant-based milk",
        "cream": "coconut cream",
        "butter": "vegan butter",
        "cheese": "dairy-free cheese",
        "yogurt": "plant-based yogurt",
        "buttermilk": "plant-based milk mixed with lemon juice or vinegar"
    }

    full_ingredient_name_transformations = {}

    # substitute ingredients
    for ingredient in parsed_recipe['ingredients']:
        ingredient_name = ingredient['name']
        for dairy, sub in lactose_free_subs.items():
            if dairy in ingredient_name:
                ingredient['name'] = sub
                if ingredient['preparation']:
                    full_ingredient_name_transformations[ingredient_name.replace(ingredient['preparation'], '').strip()] = sub
                else:
                    full_ingredient_name_transformations[ingredient_name] = sub

    # substitute steps
    for number, step in parsed_recipe['directions'].items():
        step = step.lower()

        for dairy, sub in full_ingredient_name_transformations.items():
            if dairy in step:
                parsed_recipe['directions'][number] = step.replace(dairy, sub)

    return parsed_recipe
