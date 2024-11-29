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
    descriptors = {}

    # substitute ingredients
    for ingredient in parsed_recipe['ingredients']:
        ingredient_name = ingredient['name']
        for dairy, sub in lactose_free_subs.items():
            if dairy in ingredient_name:
                ingredient['name'] = sub
                full_ingredient_name_transformations[ingredient_name] = sub
                if ingredient['descriptor']:
                    descriptors[dairy] = ingredient['descriptor']

    print(full_ingredient_name_transformations)
    print(descriptors)

    # substitute steps
    for number, step in parsed_recipe['directions'].items():
        step = step.lower()

        for dairy, sub in full_ingredient_name_transformations.items():
            if dairy in step:
                if descriptors[dairy]:
                    parsed_recipe['directions'][number] = step.replace(descriptors[dairy] + ' ' + dairy, sub)
                else:
                    parsed_recipe['directions'][number] = step.replace(dairy, sub)
                step = parsed_recipe['directions'][number]

    return parsed_recipe
