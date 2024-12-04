from directions import fetch_recipe_page
from directions import get_temperature_api
from datafetch import parse_recipe
from parserhelper import find_ingredients_in_string
from parserhelper import answer_cooking_question
from multiplier import multiply_ingredients
import string
import re

def main():
    print("Welcome to the Recipe Transformer! Please specify an AllRecipes URL.")
    user_message = input("\n> ").lower()

    url = user_message.strip('<>')
    print("Fetching recipe...")
    html_content = fetch_recipe_page(url)
    parsed_recipe = multiply_ingredients(parse_recipe(html_content), 2)

    print(parsed_recipe)

if __name__ == "__main__":
    main()
