from directions import fetch_recipe_page
from datafetch import parse_recipe
import nltk
import random

meats = ["chicken", "fish", "lamb", "beef", "pancetta", "salmon", "pork"]
meat_subs = ["vegetables", "tofu", "saitan", "tempeh", "beyond", "impossible"]
meat_parts = ["thigh", "breast", "leg"]
meat_liquids = ["broth", "stew", "stock"]

def to_vegetarian(ingredients, tools, methods, steps):
    # TRANSFORM INGREDIENTS
    choices = meat_subs[:]
    veg_dict = {}
    transformer_dict = {}
    veg_ingredients = []
    for ing in ingredients:
        veg_ing = {}
        
        amount = ing["amount"]
        unit = ing["unit"]
        descriptor = ing["descriptor"]
        preparation = ing["preparation"]

        ingredient = ing["name"]
        veg_ingredient = ingredient

        for meat in meats:
            if meat in ingredient:
                # replace
                if meat == ingredient:
                    sub_choice = choose_replacement(meat, choices)
                    transformer_dict[meat] = sub_choice
                    veg_ingredient = sub_choice
                    if len(choices) > 0:
                        choices.remove(sub_choice.split(" ")[0])

                else:
                    split = ingredient.split(meat)
                    left_side = split[0]
                    right_side = split[1]
                    is_liquid = False
                    for liq in meat_liquids:
                        if liq in right_side:
                            is_liquid = True
                            transformer_dict[meat + " " + liq] = "vegetable " + liq
                            break
                    if is_liquid:
                        veg_ingredient = "vegetable " + liq
                    else:
                        sub_choice = choose_replacement(meat, choices)
                        if len(choices) > 0:
                            choices.remove(sub_choice.split(" ")[0])
                        transformer_dict[meat] = sub_choice
                        veg_ingredient = left_side + sub_choice
                    
        
        veg_ing["amount"] = amount
        veg_ing["unit"] = unit
        veg_ing["name"] = veg_ingredient
        veg_ing["descriptor"] = descriptor
        veg_ing["preparation"] = preparation

        # print(f"original: {ing}")
        # print(f"veg version: {veg_ing}")
        # print('\n')

        veg_ingredients.append(veg_ing)
    
    
    veg_dict["ingredients"] = veg_ingredients
                    

    # TRANSFORM DIRECTIONS
    veg_steps = {}
    for step_num in steps:
        cooking_step = steps[step_num]
        # print(f"original: {cooking_step}")
        veg_step = convert_phrase_vegetarian(cooking_step, transformer_dict)
        veg_steps[step_num] = veg_step
        # print(f"veg: {veg_step}")
        # print("\n")
    
    veg_dict["directions"] = veg_steps

    # TRANSFORM TOOLS (NOT REALLY)

    veg_dict["tools"] = tools

    # TRANSFORM METHODS (NOT REALLY)

    veg_dict["methods"] = methods

    # COMBINE

    return veg_dict

def convert_phrase_vegetarian(phrase, transformer_dict):
    for meat in transformer_dict:
        if meat in phrase:
            phrase = phrase.replace(meat, transformer_dict[meat])
    for part in meat_parts:
        if part in phrase:
            plural_part = part + "s"
            phrase.replace(part, "")
            phrase.replace(plural_part, "")
    return phrase

def choose_replacement(meat, choices):
    if choices == []:
        return "vegetables"
    substitute = random.choice(choices)
    if substitute == "beyond" or substitute == "impossible":
        return substitute + " " + meat
    else:
        return substitute

    
def to_veg_transformation(parsed_dict):
    ingredients = parsed_dict["ingredients"]
    tools = parsed_dict["tools"]
    methods = parsed_dict["methods"]
    steps = parsed_dict["directions"]
    return to_vegetarian(ingredients, tools, methods, steps)

if __name__ == "__main__":
    recipe_url = "https://www.allrecipes.com/chicken-carbonara-pasta-bake-recipe-7969899"
    recipe_content = fetch_recipe_page(recipe_url)
    parsed_dict = parse_recipe(recipe_content)
    print(parsed_dict)
    ingredients = parsed_dict["ingredients"]
    tools = parsed_dict["tools"]
    methods = parsed_dict["methods"]
    steps = parsed_dict["directions"]
    print("\n")
    print(to_vegetarian(ingredients, tools, methods, steps))