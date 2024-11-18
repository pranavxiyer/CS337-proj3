import re

def find_ingredients_in_string(ingredients, input_string):
    # Normalize the ingredient names
    normalized_ingredients = []
    for ingredient in ingredients:
        name = ingredient['name']
        # Remove any additional descriptors
        name = re.sub(r',.*', '', name)  # Remove anything after a comma
        name = re.sub(r'\b\w+-\w+\b', '', name).strip()  # Remove hyphenated words
        normalized_ingredients.append({'name': name, 'original_name': ingredient['name']})

    found_ingredients = []
    for normalized in normalized_ingredients:
        if normalized['name'].lower() in input_string.lower():
            found_ingredients.append(normalized['name'])

    return found_ingredients

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import re

# Download necessary NLTK data files
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
def get_all_pos_tags(word):
    pos_tags = set()
    for synset in wordnet.synsets(word):
        pos_tags.add(synset.pos())
    return pos_tags

def answer_cooking_question(step_string, question):
    match = re.search(r'how long do I (.*)', question)
    if not match:
        return "Invalid question format."

    content = match.group(1)

    tokens = word_tokenize(content)
    # print(tokens)
    # Find the cooking verb in the question
    cooking_verb = None
    for word in tokens:
        # print(word)
        possible_pos_tags = get_all_pos_tags(word)
        if 'v'in possible_pos_tags:
            cooking_verb = word

    if not cooking_verb:
        return "No cooking verb found in the question."

    # Find the cooking verb in the step_string
    verb_index = step_string.lower().find(cooking_verb.lower())
    if verb_index == -1:
        return "The cooking verb is not found in the step string."

    relevant_part = step_string[verb_index:]

    duration_match = re.search(r'(until|for).*', relevant_part)
    if duration_match:
        duration = duration_match.group(0)
        # Clean up the duration string
        duration = duration.strip().lstrip('until').lstrip('for').strip()
        return duration
    return "No duration or condition found."





if __name__ == "__main__":
    string = "Mix in remaining 1 1/2 cups flour, remaining 1/2 cup warm water, 2 tablespoons sugar, vegetable oil, and salt."
    ingredients = [
        {'amount': '1 3/4', 'unit': 'cups', 'name': 'all-purpose flour, divided'},
        {'amount': '3/4', 'unit': 'cup', 'name': 'warm water, divided'},
        {'amount': '1', 'unit': 'tablespoon', 'name': 'active dry yeast'},
        {'amount': '1', 'unit': 'teaspoon', 'name': 'white sugar'},
        {'amount': '2', 'unit': 'tablespoons', 'name': 'white sugar'},
        {'amount': '1', 'unit': 'tablespoon', 'name': 'vegetable oil'},
        {'amount': '1/4', 'unit': 'teaspoon', 'name': 'salt'},
        {'amount': '1/2', 'unit': 'teaspoon', 'name': 'baking powder'}
    ]



    found_ingredients = find_ingredients_in_string(ingredients, string)
    # print(found_ingredients)

        
    # Examples
    step_string1 = "Knead until dough is smooth and elastic."
    question1 = "how long do I knead the dough?"
    print(answer_cooking_question(step_string1, question1))  # Output: "dough is smooth and elastic"

    step_string2 = "Allow to sit for 30 minutes."
    question2 = "how long do I let sit?"
    print(answer_cooking_question(step_string2, question2))  # Output: "30 minutes"

