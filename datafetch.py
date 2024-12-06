from bs4 import BeautifulSoup
import re
from directions import get_directions, fetch_recipe_page, get_methods_spacy
from parserhelper import extract_descriptor_and_preparation
from toolfinding import extract_tools
from unicodedata import*


def clean_text(s):
    return normalize('NFKC',s).replace(*'⁄/')
    

def get_ingredients(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    ingredients = []
    directions = []
    def has_options_class(tag):
        return tag.name == 'ul' and 'ingredients' in tag.get('class', [])

    ingLists = soup.find_all(name='ul', class_=re.compile('ingredients'))
    
    for ingListText in ingLists:
        for text in ingListText.find_all('p'):
            ing = {}
            for spanner in text.find_all('span'):
                if spanner.has_attr("data-ingredient-quantity"):
                    ing["amount"] = clean_text(spanner.text)
                elif spanner.has_attr("data-ingredient-unit"):
                    ing["unit"] = clean_text(spanner.text)
                elif spanner.has_attr("data-ingredient-name"):
                    ing["name"] = clean_text(spanner.text)
            # print(ing["name"])
            descriptor, preparation = extract_descriptor_and_preparation(ing["name"])

            if not descriptor:
                descriptor = ""
            if not preparation:
                preparation = ""

            name = ing["name"]    

            pattern = re.compile(r'\b' + re.escape(descriptor) + r'\b|\b' + re.escape(preparation) + r'\b', re.IGNORECASE)

            cleaned_name = pattern.sub('', name).strip()

            # Remove any trailing commas or extra spaces
            ing["name"] = re.sub(r',\s*$', '', cleaned_name).strip()

            ing["descriptor"] = descriptor
            ing["preparation"] = preparation
            ingredients.append(ing)

    return ingredients

def parse_recipe(html_content):
    ingredients = get_ingredients(html_content)
    directions = get_directions(html_content)
    tools = extract_tools(list(directions.values()))
    methods = get_methods_spacy(directions)
    print(list(directions.values()))
    return {
        'ingredients': ingredients,
        'directions': directions,
        'tools': tools,
        'methods': methods
    }


if __name__ == "__main__":

    # Example usage
    url = "https://www.allrecipes.com/recipe/72114/chicken-souvlaki-gyro-style/"
    # url = "https://www.seriouseats.com/baked-french-toast-casserole-recipe-8740716"
    html_content = fetch_recipe_page(url)

    # Example usage
    recipe_data = parse_recipe(html_content)
    print(recipe_data)
    # print()
    # cleaner = lambda s:normalize('NFKC',s).replace(*'⁄/')
        

    # for ingredient in recipe_data['ingredients']:
    #     if ing in ingredient["name"]:
    #         print(f"You need: {ingredient}")

    # print(recipe_data["ingredients"][0]["name"])
    
    
    # ing = "brioche"

    # ingredient_name = ing
    # for ingredient in recipe_data['ingredients']:
    #     if ingredient_name in ingredient["name"]:
    #         amt = ingredient['amount']
    #         unit = ingredient['unit']
    #         ingr_name = ingredient['name']
            
    #         print(f"You need: {amt} {unit} of {ingr_name}")

