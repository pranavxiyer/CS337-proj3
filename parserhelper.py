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
from nltk.corpus import wordnet
import re
from rapidfuzz import fuzz
from directions import get_first_cooking_verb

def get_all_pos_tags(word):
    pos_tags = set()
    for synset in wordnet.synsets(word):
        pos_tags.add(synset.pos())
    return pos_tags

def how_long_til_done(step_string, question):
    if not fuzz.token_sort_ratio(question, "When is done") > 0.70:
        return "Invalid question format."
    duration_match = re.search(r'(until|for).*', step_string)
    if duration_match:
        duration = duration_match.group(0)
        # Clean up the duration string
        duration = duration.strip().lstrip('until').lstrip('for').strip()
        return duration
    return "No duration or condition found."



def answer_cooking_question(step_string, question):
    match = re.search(r'how long do i (.*)', question)
    if not match:
        return how_long_til_done(step_string, question)

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


def extract_descriptor_and_preparation(ingredient):
    # Define lists of common descriptors and preparations
    descriptors = ['fresh', 'extra-virgin', 'dried', 'canned', 'frozen', 'organic', 'whole', 'ground']
    preparations = ['divided', 'finely chopped', 'chopped', 'sliced', 'diced', 'minced', 'crushed', 'grated', 'shredded', 'peeled', 'cored', 'seeded']

    # Tokenize the ingredient string
    tokens = word_tokenize(ingredient)

    # POS tagging to identify adjectives (descriptors) and verbs (preparations)
    pos_tags = nltk.pos_tag(tokens)

    # Initialize variables to store the descriptor and preparation
    descriptor = None
    preparation = None

    # Iterate through the POS tags to find descriptors and preparations
    for word, tag in pos_tags:
        if tag.startswith('JJ') and word in descriptors:  # Adjectives
            descriptor = word
        elif tag.startswith('V') : #and any(prep.startswith(word) for prep in preparations):  # Verbs
            preparation = next((prep for prep in preparations if prep.startswith(word)), None)

    return descriptor, preparation




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

    
    # Example usage
    ingredient = 'all-purpose flour, divided'
    descriptor, preparation = extract_descriptor_and_preparation(ingredient)
    print(f"Descriptor: {descriptor}, Preparation: {preparation}")

    ingredient = 'fresh basil, finely chopped'
    descriptor, preparation = extract_descriptor_and_preparation(ingredient)
    print(f"Descriptor: {descriptor}, Preparation: {preparation}")


    found_ingredients = find_ingredients_in_string(ingredients, string)
    # print(found_ingredients)

        
    # Examples
    step_string1 = "Knead until dough is smooth and elastic."
    question1 = "how long do I knead the dough?"
    print(answer_cooking_question(step_string1, question1))  # Output: "dough is smooth and elastic"

    step_string2 = "Allow to sit for 30 minutes."
    question2 = "When is it done?"
    print(answer_cooking_question(step_string2, question2))  # Output: "30 minutes"

