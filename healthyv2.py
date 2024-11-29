import spacy
from nltk.corpus import wordnet
import nltk

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def get_healthier_alternative(ingredient):
    
    unhealthy_to_healthy = {
        'sugar': 'honey',
        'butter': 'olive oil',
        'white flour': 'whole wheat flour',
        'salt': 'herbs',
        'cream': 'low-fat yogurt',
        'mayonnaise': 'greek yogurt',
        'bacon': 'turkey bacon',
        'beef': 'chicken',
        'sausage': 'turkey sausage',
        'milk': 'almond milk',
        'cheese': 'low-fat cheese',
        'oil': 'olive oil'
    }
    doc = nlp(ingredient.lower())
    tokens = [token.lemma_ for token in doc]

    # Check for partial matches or synonyms
    for token in tokens:
        for unhealthy, healthy in unhealthy_to_healthy.items():
            if token in unhealthy:
                return ingredient.replace(token, healthy)

            # Check for synonyms using WordNet
            synsets = wordnet.synsets(token)
            for synset in synsets:
                for lemma in synset.lemmas():
                    if lemma.name() in unhealthy:
                        return ingredient.replace(token, healthy)

    return ingredient


def make_recipe_healthier(recipe):
    
    for ingredient in recipe['Ingredients']:
        name = ingredient['name']
        healthier_name = get_healthier_alternative(name)
        if healthier_name != name:
            ingredient['name'] = healthier_name
            ingredient['descriptor'] = 'healthier'


    primary_methods = recipe['Methods'][0]
    secondary_methods = recipe['Methods'][1]

    healthier_methods = {
        'fry': 'bake',
        'sauté': 'stir-fry',
        'deep-fry': 'air-fry',
        'boil': 'steam'
    }

    for i, method in enumerate(primary_methods):
        if method.lower() in healthier_methods:
            primary_methods[i] = healthier_methods[method.lower()]

    for i, method in enumerate(secondary_methods):
        if method.lower() in healthier_methods:
            secondary_methods[i] = healthier_methods[method.lower()]

    # Update the recipe with healthier methods
    recipe['Methods'] = [primary_methods, secondary_methods]

    # Process steps (optional, depending on complexity)
    for step in recipe['Steps']:
        doc = nlp(step)
        for token in doc:
            if token.lemma_ in healthier_methods:
                step = step.replace(token.text, healthier_methods[token.lemma_])

    return recipe

# Example usage
recipe = {
    'Ingredients': [
        {'name': 'butter', 'amount': 1, 'measurement': 'cup', 'descriptor': 'unsalted', 'preparation': 'melted'},
        {'name': 'sugar', 'amount': 2, 'measurement': 'cups', 'descriptor': 'granulated', 'preparation': 'none'},
        {'name': 'flour', 'amount': 3, 'measurement': 'cups', 'descriptor': 'all-purpose', 'preparation': 'sifted'}
    ],
    'Tools': ['pan', 'whisk'],
    'Methods': [['sauté'], ['stir', 'mix']],
    'Steps': [
        'Melt the butter in a pan.',
        'Add the sugar and stir until dissolved.',
        'Gradually add the flour and mix well.'
    ]
}

healthier_recipe = make_recipe_healthier(recipe)
print(healthier_recipe)
