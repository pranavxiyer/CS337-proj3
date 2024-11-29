import spacy
from nltk.corpus import wordnet
import nltk

# nltk.download('wordnet')
# nltk.download('omw-1.4')

nlp = spacy.load('en_core_web_sm')

def get_healthier_alternative(ingredient):
    
    ingr = ingredient['name'].lower()

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
    for unhealthy, healthy in unhealthy_to_healthy.items():
        if unhealthy in ingr:
            ingredient['name'] = healthy
            return healthy

        synsets = wordnet.synsets(unhealthy)
        for synset in synsets:
            for lemma in synset.lemmas():
                if lemma.name() in ingr:
                    return healthy

    return ingredient


def make_recipe_healthier(recipe):
    
    for ingredient in recipe['ingredients']:
        ingredient = get_healthier_alternative(ingredient)
        # name = ingredient['name']
        # healthier_name = get_healthier_alternative(name)
        # if healthier_name != name:
        #     ingredient['name'] = healthier_name

    methods = list(recipe['methods'])
    primary_methods = list(methods[0])
    secondary_methods = list(methods[1])

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

    recipe['methods'] = [primary_methods, secondary_methods]

    for step in recipe['directions']:
        doc = nlp(step)
        for token in doc:
            if token.lemma_ in healthier_methods:
                step = step.replace(token.text, healthier_methods[token.lemma_])

    return recipe



if __name__ == "__main__":
    # Example usage
    recipe = {
        'ingredients': [
            {'amount': '1 3/4', 'unit': 'cups', 'name': 'all-purpose flour, divided', 'descriptor': 'all-purpose', 'preparation': 'divided'}, 
            {'amount': '3/4', 'unit': 'cup', 'name': 'warm water, divided', 'descriptor': 'warm', 'preparation': 'divided'}, 
            {'amount': '1', 'unit': 'tablespoon', 'name': 'active dry yeast', 'descriptor': 'dry', 'preparation': None}, 
            {'amount': '1', 'unit': 'teaspoon', 'name': 'white sugar', 'descriptor': 'white', 'preparation': None}, 
            {'amount': '2', 'unit': 'tablespoons', 'name': 'white sugar', 'descriptor': 'white', 'preparation': None}, 
            {'amount': '1', 'unit': 'tablespoon', 'name': 'vegetable oil', 'descriptor': 'vegetable', 'preparation': None}, 
            {'amount': '1/4', 'unit': 'teaspoon', 'name': 'salt', 'descriptor': None, 'preparation': None}, 
            {'amount': '1/2', 'unit': 'teaspoon', 'name': 'baking powder', 'descriptor': None, 'preparation': None}
        ],
        'directions': {
            'Step 1': 'Gather all ingredients.', 
            'Step 2': 'Mix together 1/4 cup flour, 1/4 cup warm water, yeast, and 1 teaspoon sugar in a large bowl.', 
            'Step 3': 'Allow to sit for 30 minutes.', 
            'Step 4': 'Mix in remaining 1 1/2 cups flour, remaining 1/2 cup warm water, 2 tablespoons sugar, vegetable oil, and salt.', 
            'Step 5': 'Knead until dough is smooth and elastic.', 
            'Step 6': 'Transfer to a greased bowl, roll to coat with oil, and let sit until tripled in size, 2 1/2 to 3 hours.', 
            'Step 7': 'Punch down dough and spread out on a floured board.', 'Step 8': 'Sprinkle baking powder evenly on surface of dough; knead for 5 minutes.', 'Step 9': 'Divide dough in half; set aside one half in a covered bowl.', 'Step 10': 'Divide remaining half into 12 equal pieces.', 'Step 11': 'Shape each into a ball; transfer each ball to a small square of waxed paper with the smooth surface facing up.', 'Step 12': 'Repeat portioning and shaping with remaining dough half.', 'Step 13': 'Cover all 24 dough balls and let sit until doubled in size, about 30 minutes.', 'Step 14': 'Bring some water to a boil in a wok, then reduce heat to medium and keep water at a low boil.', 'Step 15': 'Place the steam plate on a small wire rack in the middle of the wok, leaving at least 2 inches of space between the plate and the wok.', 'Step 16': 'Working in batches, place buns on waxed paper squares onto the steam plate, leaving 1 to 2 inches between buns.', 'Step 17': 'Cover and steam buns for 15 minutes.', 'Step 18': "Carefully remove the lid, so condensation doesn't drip onto buns.", 'Step 19': 'Continue steaming remaining buns until all are cooked.'
        }, 
        'tools': ['plate', 'bowl', 'wok'], 
        'methods': 
            ({'cook', 'bake', 'steam', 'heat', 'boil'}, {'leave', 'allow', 'punch', 'mix', 'reduce', 'work', 'keep', 'bring', 'set', 'sprinkle', 'spread', 'transfer', 'gather', 'triple', 'cover', 'let', 'wax', 'divide', 'roll', 'shape', 'face', 'double', 'drip', 'knead', 'continue', 'repeat', 'sit', 'remain', 'place', 'remove'})}


    healthier_recipe = make_recipe_healthier(recipe)
    print(healthier_recipe)
