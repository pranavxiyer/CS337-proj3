import requests
from bs4 import BeautifulSoup
import spacy
import nltk
from nltk.corpus import verbnet
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from rapidfuzz import fuzz
import re
# nltk.download('verbnet')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')
spacy_model = spacy.load("en_core_web_lg")
cooking_class = verbnet.vnclass('cooking-45.3')
method_verbs = [member.get("name") for member in cooking_class.findall("MEMBERS/MEMBER")]

# methods = ["poach", "deep fry", "shallow fry", "steam", "sautee", "bast", "boil", "blanch", "broil", "stew", 
#            "grill", "bake", "barbeque", "ovenroast", "braise", "pressure cook", "skillet cook"]

def fetch_recipe_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

def get_directions(html_content):
    directions = {}
    directions_list = []
    soup = BeautifulSoup(html_content, 'html.parser')
    direction_results = soup.find(id="mm-recipes-steps_1-0")
    direction_ol = direction_results.find("ol")
    direction_li = direction_ol.find_all("li")
    
    for i in range(len(direction_li)):
        p = direction_li[i].find("p")
        step_direction = p.text.strip()
        step_split = step_direction.split(".")

        for j in range(len(step_split)):
            if len(step_split[j]) > 1:
                real_step_direction = step_split[j].lstrip() + "."
                directions_list.append(real_step_direction)
    
    for i in range(len(directions_list)):
        real_step = i + 1
        step_text = "Step " + str(real_step)
        directions[step_text] = directions_list[i]

    return directions

def get_cooks_note():
    return None

def get_methods_nltk(directions_dictionary):
    primary_methods = set()
    secondary_methods = set()
    for step in directions_dictionary:
        step_dir = directions_dictionary[step]
        tokenized_dir = nltk.word_tokenize(step_dir.lower())
        pos = nltk.pos_tag(tokenized_dir)
        for token in tokenized_dir:
            present_form = WordNetLemmatizer().lemmatize(token, 'v')
            if present_form in method_verbs:
                primary_methods.add(present_form)
            else:
                synset = wn.synsets(token)
                for syn in synset:
                    if syn.pos() == 'v':
                        secondary_methods.add(present_form)

    # print(f"primary: {primary_methods}")
    # print(f"secondary: {secondary_methods}")

    return primary_methods, secondary_methods

def get_methods_spacy(directions_dictionary):
    primary_methods = set()
    secondary_methods = set()
    for step in directions_dictionary:
        step_dir = directions_dictionary[step]
        spacy_output = spacy_model(step_dir)
        for token in spacy_output:
            #print(token.text, token.pos_)
            present_form = WordNetLemmatizer().lemmatize(token.text.lower(), 'v')
            if present_form in method_verbs:
                primary_methods.add(present_form)
            else:
                if token.pos_ == "VERB":
                    secondary_methods.add(present_form)

    # print(f"primary: {primary_methods}")
    # print(f"secondary: {secondary_methods}")

    return primary_methods, secondary_methods

def get_first_cooking_verb(sentence):
    spacy_output = spacy_model(sentence)
    for token in spacy_output:
        if token.pos_ == "VERB":
            return token.text.lower()
    return None

def get_temperature_num(sentence):
    num_temps = []
    spacy_output = spacy_model(sentence)
    for token in spacy_output:
        if token.like_num:
            num_temps.append(token.text)

    tokenized_sentence = nltk.word_tokenize(sentence.lower())

    temp_phrases = []

    for i in range(len(tokenized_sentence)):
        if tokenized_sentence[i] in num_temps or re.search(r'\d+', tokenized_sentence[i]):
            if '°' in tokenized_sentence[i]:
                temp_phrase = tokenized_sentence[i]
                temp_phrases.append(temp_phrase)
            elif i + 2 in range(len(tokenized_sentence)):
                if tokenized_sentence[i+1] in "degrees":
                    temp_phrase = tokenized_sentence[i] + " " + tokenized_sentence[i+1] + " " + tokenized_sentence[i+2]
                    temp_phrases.append(temp_phrase)

                elif '°' in tokenized_sentence[i+1]:
                    temp_phrase = tokenized_sentence[i] + " " + tokenized_sentence[i+1]
                    temp_phrases.append(temp_phrase)
    return temp_phrases

def get_temperature_regular(sentence):
    temp_keywords = ["low", "medium", "high", "rare", "well", "done", "al", "dente"]
    tokenized_sentence = nltk.word_tokenize(sentence.lower())
    for i in range(len(tokenized_sentence)):
        token = tokenized_sentence[i]
        for keyword in temp_keywords:
            if keyword in token:
                if i + 1 in range(len(tokenized_sentence)):
                    if any(keyword in tokenized_sentence[i + 1] for keyword in temp_keywords):
                        return tokenized_sentence[i] + " " + tokenized_sentence[i + 1]
                    else:
                        if token == 'al':
                            break
                        return token
                else:
                    return token 
    return None

def get_temperature_api(sentence):
    temp_nums = get_temperature_num(sentence)
    word = get_temperature_regular(sentence)
    if len(temp_nums) > 0 and word:
        return temp_nums, word
    elif len(temp_nums) > 0:
        return temp_nums
    elif word:
        return [word]
    else:
        return "no temperature"

# recipe_url = "https://www.allrecipes.com/recipe/8462067/spinach-artichoke-garlic-naan-pizza"
# recipe_url = "https://www.allrecipes.com/chicken-carbonara-pasta-bake-recipe-7969899"
# recipe_url = "https://www.allrecipes.com/recipe/7011/chinese-steamed-buns/"

