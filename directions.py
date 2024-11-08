import requests
from bs4 import BeautifulSoup

def fetch_recipe_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

def get_directions(html_content):
    directions = {}
    soup = BeautifulSoup(html_content, 'html.parser')
    direction_results = soup.find(id="mm-recipes-steps_1-0")
    direction_p = direction_results.find_all('p')
    for step in direction_p:
        print(step.text)

# recipe_url = "https://www.allrecipes.com/recipe/8462067/spinach-artichoke-garlic-naan-pizza"
recipe_url = "https://www.allrecipes.com/chicken-carbonara-pasta-bake-recipe-7969899"
recipe_html = fetch_recipe_page(recipe_url)
get_directions(recipe_html)