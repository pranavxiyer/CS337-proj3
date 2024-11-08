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
    for text in soup.find_all('p'):
        if not (text.string):
            print(text)
            
            print(text.span.string)

    # Extracting ingredients
    ingredients = []
    for ingredient in soup.select('.recipe-ingred_txt'):
        ingredient_text = ingredient.get_text()
        ingredients.append(ingredient_text)

    # Extracting directions
    directions = []
    for direction in soup.select('.recipe-directions__list--item'):
        direction_text = direction.get_text()
        directions.append(direction_text)

    # Extracting tools and methods (optional)
    tools = []
    methods = []
    # This part will depend on the specific HTML structure of the website
    # and might require more sophisticated parsing logic.

    return {
        'ingredients': ingredients,
        'directions': directions,
        'tools': tools,
        'methods': methods
    }

# Example usage
url = "https://www.allrecipes.com/recipe/246481/slow-cooked-red-braised-pork-belly/"
html_content = fetch_recipe_page(url)

# Example usage
recipe_data = parse_recipe(html_content)
# print(html_content)
