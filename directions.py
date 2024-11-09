import requests
from bs4 import BeautifulSoup
import spacy
import nltk
from nltk.corpus import verbnet

spacy_model = spacy.load("en_core_web_sm")
cooking_class = verbnet.vnclass('cooking-45.3')
method_verbs = [member.get("name") for member in cooking_class.findall("MEMBERS/MEMBER")]

print(method_verbs)

methods = ["poach", "deep fry", "shallow fry", "steam", "sautee", "bast", "boil", "blanch", "broil", "stew", 
           "grill", "bake", "barbeque", "ovenroast", "braise", "pressure cook", "skillet cook"]

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
    direction_ol = direction_results.find("ol")
    direction_li = direction_ol.find_all("li")
    
    for i in range(len(direction_li)):
        p = direction_li[i].find("p")
        real_step = i + 1
        step_text = "Step " + str(real_step)
        step_direction = p.text.strip()
        directions[step_text] = step_direction
    
    return directions

def get_cooks_note():
    return None

def get_methods(directions_dictionary):
    methods = []
    for step in directions_dictionary:
        step_dir = directions_dictionary[step]
        print(step_dir)
        tokenized_dir = nltk.word_tokenize(step_dir.lower())
        pos = nltk.pos_tag(tokenized_dir)
        for word in pos:
            print(word)
        # verbs = [word for word, tag in pos if tag.startswith('VB')]
        # for verb in verbs:
        #     if verb not in methods:
        #         methods.append(verb.lower())
        # spacy_output = spacy_model(step_dir)
        # for token in spacy_output:
        #     if token.pos_ == "VERB":
        #         if token.text not in methods:
        #             methods.append(token.text.lower())
                # print(token.text, token.pos_)
    print(methods)

# recipe_url = "https://www.allrecipes.com/recipe/8462067/spinach-artichoke-garlic-naan-pizza"
recipe_url = "https://www.allrecipes.com/chicken-carbonara-pasta-bake-recipe-7969899"
recipe_html = fetch_recipe_page(recipe_url)
directions = get_directions(recipe_html)
get_methods(directions)
