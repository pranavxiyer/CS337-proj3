import spacy
from nltk.corpus import wordnet
import nltk

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load spaCy model
import en_core_web_sm
nlp = en_core_web_sm.load()


# Define a function to get healthier alternatives
def get_healthier_alternative(ingredient):
    # Example mappings (this can be expanded)
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

# Define a function to suggest healthier transformations
def suggest_healthier_transformations(recipe):
    suggestions = []

    # Process ingredients
    for ingredient in recipe['Ingredients']:
        name = ingredient['name']
        healthier_name = get_healthier_alternative(name)
        if healthier_name:
            suggestions.append(f"Substitute {name} with {healthier_name}.")

    # Process methods
    primary_methods = recipe['Methods'][0]
    secondary_methods = recipe['Methods'][1]

    healthier_methods = {
        'fry': 'bake',
        'sauté': 'stir-fry',
        'deep-fry': 'air-fry',
        'boil': 'steam'
    }

    for method in primary_methods:
        if method.lower() in healthier_methods:
            suggestions.append(f"Replace {method} with {healthier_methods[method.lower()]}.")

    for method in secondary_methods:
        if method.lower() in healthier_methods:
            suggestions.append(f"Replace {method} with {healthier_methods[method.lower()]}.")

    # Process steps (optional, depending on complexity)
    for step in recipe['Steps']:
        doc = nlp(step)
        for token in doc:
            if token.lemma_ in healthier_methods:
                suggestions.append(f"In the step '{step}', replace {token.text} with {healthier_methods[token.lemma_]}.")

    return suggestions




if __name__ == "__main__":
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

    suggestions = suggest_healthier_transformations(recipe)
    for suggestion in suggestions:
        print(suggestion)
