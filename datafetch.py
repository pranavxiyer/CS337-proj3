import requests
from bs4 import BeautifulSoup

def fetch_recipe_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")
def parse_recipe(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.title.string)
    # print(len(soup.find_all('p')))
    ingredients = []
    directions = []
    for text in soup.find_all('p'):
        if not (text.string):
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
        else:
            directions


    tools = []
    methods = []

    return {
        'ingredients': ingredients,
        'directions': directions,
        'tools': tools,
        'methods': methods
    }

# Example usage
url = "https://www.allrecipes.com/recipe/7011/chinese-steamed-buns/"
html_content = fetch_recipe_page(url)

# Example usage
recipe_data = parse_recipe(html_content)
print(recipe_data)
