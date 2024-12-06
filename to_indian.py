from directions import fetch_recipe_page
from datafetch import parse_recipe
import nltk
import random

change_to_indian = {"garlic": "turmeric", "thyme": "ajwain", "rosemary": "elaichi", "oregano": "coriander", "feta": "paneer",
                    "lamb": "chickpea", "beef": "chicken", "pork": "chicken", "soy sauce": "tamarind sauce", 
                    "tzatziki": "raita"}

def to_indian(recipe_dict):
    # TRANSFORM INGREDIENTS
    ingredients = parsed_dict["ingredients"]
    tools = parsed_dict["tools"]
    methods = parsed_dict["methods"]
    steps = parsed_dict["directions"]

    
    indian_dict = {}
    indian_ingredients = []
    for ing in ingredients:
        indian_ing = {}
        
        amount = ing["amount"]
        unit = ing["unit"]
        descriptor = ing["descriptor"]
        preparation = ing["preparation"]

        ingredient = ing["name"]
        indian_ingredient = ingredient

        for to_change in change_to_indian:
            if to_change in ingredient:
                # replace
                sub_choice = change_to_indian[to_change]
                indian_ingredient = sub_choice
                    
        
        indian_ing["amount"] = amount
        indian_ing["unit"] = unit
        indian_ing["name"] = indian_ingredient
        indian_ing["descriptor"] = descriptor
        indian_ing["preparation"] = preparation

        # print(f"original: {ing}")
        # print(f"veg version: {veg_ing}")
        # print('\n')

        indian_ingredients.append(indian_ing)
    
    
    indian_dict["ingredients"] = indian_ingredients

    # TRANSFORM DIRECTIONS
    indian_steps = {}
    for step_num in steps:
        cooking_step = steps[step_num]
        # print(f"original: {cooking_step}")
        indian_step = convert_phrase_indian(cooking_step, change_to_indian)
        indian_steps[step_num] = indian_step
        # print(f"veg: {veg_step}")
        # print("\n")
    
    indian_dict["directions"] = indian_steps

    # TRANSFORM TOOLS (NOT REALLY)

    indian_dict["tools"] = tools

    # TRANSFORM METHODS (NOT REALLY)

    indian_dict["methods"] = methods

    # COMBINE

    return indian_dict

def convert_phrase_indian(phrase, transformer_dict):
    for to_change in transformer_dict:
        if to_change in phrase:
            phrase = phrase.replace(to_change, transformer_dict[to_change])
    return phrase

if __name__ == "__main__":
    recipe_url = "https://www.allrecipes.com/recipe/240559/traditional-gyros/"
    recipe_content = fetch_recipe_page(recipe_url)
    parsed_dict = parse_recipe(recipe_content)
    ingredients = parsed_dict["ingredients"]
    tools = parsed_dict["tools"]
    methods = parsed_dict["methods"]
    steps = parsed_dict["directions"]

    indian_dict = to_indian(parsed_dict)

    indian_dict_ingredients = indian_dict["ingredients"]
    print(ingredients)
    print("\n")
    print(indian_dict_ingredients)

    print("\n")
    print("\n")
    
    indian_dict_tools = indian_dict["tools"]
    print(tools)
    print("\n")
    print(indian_dict_tools)

    print("\n")
    print("\n")

    indian_dict_methods = indian_dict["methods"]
    print(methods)
    print("\n")
    print(indian_dict_methods)

    print("\n")
    print("\n")

    indian_dict_steps = indian_dict["directions"]
    print(steps)
    print("\n")
    print(indian_dict_steps)