import requests
from bs4 import BeautifulSoup
import re
from directions import get_directions, fetch_recipe_page 
from toolfinding import extract_tools

def get_ingredients(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.title.string)
    # print(len(soup.find_all('p')))
    ingredients = []
    directions = []
    # Define a function to check if 'options' is in the class attribute
    def has_options_class(tag):
        return tag.name == 'ul' and 'ingredients' in tag.get('class', [])

    # Use the find method with the custom function
    ingListText = soup.find(name='ul', class_=re.compile('ingredients'))
    # print(ingListText)


    # ingListText = soup.find_all('ul')[0]
    # # ulists = 
    # for ulist in soup.find_all('ul'):
    #     if not ulist.has_attr('class'):
    #         continue
    #     elif 'ingredients' in ulist['class'][0]:
    #         ingListText = ulist
    #         break
    # print(ingListText)
    for text in ingListText.find_all('p'):
        ing = {}
        # print(text)
        # print(text.span.string)
        for spanner in text.find_all('span'):
            if spanner.has_attr("data-ingredient-quantity"):
                ing["amount"] = spanner.text
            elif spanner.has_attr("data-ingredient-unit"):
                ing["unit"] = spanner.text
            elif spanner.has_attr("data-ingredient-name"):
                ing["name"] = spanner.text
        ingredients.append(ing)

    return ingredients

def parse_recipe(html_content):
    tools = []
    methods = []
    directions = get_directions(html_content)
    # print(list(directions.values()))
    return {
        'ingredients': get_ingredients(html_content),
        'directions': directions,
        'tools': extract_tools(list(directions.values())),
        'methods': methods
    }

# Example usage
url = "https://www.allrecipes.com/recipe/7011/chinese-steamed-buns/"
# url = "https://www.seriouseats.com/baked-french-toast-casserole-recipe-8740716"
html_content = fetch_recipe_page(url)

# Example usage
recipe_data = parse_recipe(html_content)
print(recipe_data)
