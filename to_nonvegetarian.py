from directions import fetch_recipe_page
from datafetch import parse_recipe
import nltk
import random

vegetables = ["cauliflower", "bean", "potato", "carrot", "broccoli", "falafel", "pea", "radish"]
meat_list = ["chicken", "beef", "lamb"]

def to_nonvegetarian(ingredients, tools, methods, steps):
    # TRANSFORM INGREDIENTS
    transform_num = 0
    transformer_dict = {}
    nonveg_dict = {}
    nonveg_ingredients = []

    for ing in ingredients:
        nonveg_ing = {}
        amount = ing["amount"]
        unit = ing["unit"]
        descriptor = ing["descriptor"]
        preparation = ing["preparation"]

        ingredient = ing["name"]

        nonveg_ing["amount"] = amount
        nonveg_ing["unit"] = unit
        nonveg_ing["name"] = ingredient
        nonveg_ing["descriptor"] = descriptor
        nonveg_ing["preparation"] = preparation

        for veg_option in vegetables:
            if transform_num > 0:
                break
            elif veg_option in ingredient:
                transform_num += 1
                detailed_ingredient = descriptor + " " + veg_option
                meat_to_use = choose_replacement(meat_list)
                transformer_dict[veg_option] = meat_to_use
                transformer_dict[detailed_ingredient] = meat_to_use
                nonveg_ing["name"] = meat_to_use
                nonveg_ing["descriptor"] = ""
        
        nonveg_ingredients.append(nonveg_ing)
    
    nonveg_dict["ingredients"] = nonveg_ingredients

    # TRANSFORM DIRECTIONS
    nonveg_steps = {}
    for step_num in steps:
        cooking_step = steps[step_num]
        # print(f"original: {cooking_step}")
        nonveg_step = convert_phrase_nonvegetarian(cooking_step, transformer_dict)
        nonveg_steps[step_num] = nonveg_step
        # print(f"veg: {veg_step}")
        # print("\n")
    
    nonveg_dict["directions"] = nonveg_steps

    # TRANSFORM TOOLS (NOT REALLY)

    nonveg_dict["tools"] = tools

    # TRANSFORM METHODS (NOT REALLY)

    nonveg_dict["methods"] = methods

    # COMBINE
    return nonveg_dict


def convert_phrase_nonvegetarian(phrase, transformer_dict):
    for to_replace in transformer_dict:
        if to_replace in phrase:
            plural_toreplace = to_replace + "s"
            phrase = phrase.replace(plural_toreplace, transformer_dict[to_replace])
            phrase = phrase.replace(to_replace, transformer_dict[to_replace])
    return phrase

def choose_replacement(meats):
    substitute = random.choice(meats)
    return substitute

def to_veg_transformation(parsed_dict):
    ingredients = parsed_dict["ingredients"]
    tools = parsed_dict["tools"]
    methods = parsed_dict["methods"]
    steps = parsed_dict["directions"]
    return to_nonvegetarian(ingredients, tools, methods, steps)

if __name__ == "__main__":
    recipe_url = "https://www.allrecipes.com/green-bean-mac-and-cheese-recipe-8753390"
    recipe_content = fetch_recipe_page(recipe_url)
    parsed_dict = parse_recipe(recipe_content)
    ingredients = parsed_dict["ingredients"]
    tools = parsed_dict["tools"]
    methods = parsed_dict["methods"]
    steps = parsed_dict["directions"]

    nonveg_dict = to_nonvegetarian(ingredients, tools, methods, steps)

    nonveg_dict_ingredients = nonveg_dict["ingredients"]
    print(ingredients)
    print("\n")
    print(nonveg_dict_ingredients)

    print("\n")
    print("\n")
    
    nonveg_dict_tools = nonveg_dict["tools"]
    print(tools)
    print("\n")
    print(nonveg_dict_tools)

    print("\n")
    print("\n")

    nonveg_dict_methods = nonveg_dict["methods"]
    print(methods)
    print("\n")
    print(nonveg_dict_methods)

    print("\n")
    print("\n")

    nonveg_dict_steps = nonveg_dict["directions"]
    print(steps)
    print("\n")
    print(nonveg_dict_steps)
