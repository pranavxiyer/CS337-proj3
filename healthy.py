import spacy
from nltk.corpus import wordnet
import nltk
from rapidfuzz import fuzz
# nltk.download('wordnet')
# nltk.download('omw-1.4')

nlp = spacy.load('en_core_web_lg')



def replacementIngredients(conversion = 'unhealthy'):
    if conversion == 'unhealthy':
        return {
            'honey': 'sugar',
            'olive oil': 'canola oil',
            'whole wheat flour': 'white bleached flour',
            'salt': 'msg',
            'low-fat yogurt': 'cream',
            'greek yogurt': 'full-fat sour cream',
            'chicken breast': 'bacon-wrapped sausages',
            'berries': 'fruit gummies',
            'avocado': 'mayonnaise',
            'broth': 'bouillon cubes',
            'stock': 'bouillon cubes',
            'turkey sausage': 'sausage',
            'almond milk': 'milk',
            'low-fat cheese': 'cheese',
            'oil': 'butter'
        }
    else:
        return {
            'sugar': 'honey',
            'butter': 'olive oil',
            'flour': 'whole wheat flour',
            'cream': 'low-fat yogurt',
            'monosodium glutamate': ['shiitake mushrooms',  'powdered', None],
            'MSG': ['shiitake mushrooms',  'powdered', None],
            'mayonnaise': 'greek yogurt',
            'beef': 'chicken',
            'milk': 'almond milk',
            'cheese': 'low-fat cheese',
            'oil': 'olive oil'
        }
    
def replacementMethods(conversion = 'unhealthy'):
    if conversion == 'unhealthy':
        return {
            'pan fry': 'deep-fry',
            'air-fry': 'deep-fry',
            'fry': 'deep-fry'
        }
    else:
        return {
            'deep': 'air',
            'stir-fry': 'sauté',
            'boil': 'steam'
        }


def get_ingredient_alternative(ingredient, transform):
    
    ingr = ingredient['name'].lower()

    for original, replacement in replacementIngredients(transform).items():
        if fuzz.token_set_ratio(original, ingr) > 90:
            if type(replacement) == list:
                ingredient['name'] = replacement[0]
                ingredient['descriptor'] = replacement[1]
                ingredient['preparation'] = replacement[2] if replacement[2] is not None else ingredient['preparation']
                return ingredient
            
            ingredient['name'] = replacement
            ingredient['descriptor'] = ''
            return ingredient

        synsets = wordnet.synsets(original)
        for synset in synsets:
            for lemma in synset.lemmas():
                if lemma.name() in ingr:
                    ingredient['name'] = replacement
                    ingredient['descriptor'] = ''
                    return ingredient

    return ingredient

def formatIngRepl(ingr):
    if isinstance(ingr, list):
        if len(ingr) > 1:
            return f"{ingr[1]} {ingr[0]}"
        return ingr[0]
    return ingr



def transform_recipe_healthiness(recipe, transform):
    
    for ingredient in recipe['ingredients']:
        ingredient = get_ingredient_alternative(ingredient, transform)
        

    methods = list(recipe['methods'])
    primary_methods = list(methods[0])
    secondary_methods = list(methods[1])

    replacement_methods = replacementMethods(transform)

    for i, method in enumerate(primary_methods):
        for replacement in replacement_methods:
            if fuzz.token_set_ratio(replacement, method) > 90:
                secondary_methods[i] = replacement_methods[replacement]

    for i, method in enumerate(secondary_methods):
        for replacement in replacement_methods:
            if fuzz.token_set_ratio(replacement, method) > 90:
                secondary_methods[i] = replacement_methods[replacement]

    recipe['methods'] = [set(primary_methods), set(secondary_methods)]

    for iter, step in recipe['directions'].items():
        doc = nlp(step)
        for token in doc:
            if method in replacement_methods:
                if (token.lemma_, method) > 90:
                    step = step.replace(token.text, replacement_methods[method])
            replIngs = replacementIngredients(transform)
            for repling in replIngs:
                if fuzz.token_set_ratio(token.lemma_, repling) > 90:
                    # print("_______________" + replIngs[token.lemma_])
                    step = step.replace(token.text, formatIngRepl(replIngs[repling]))
        #         print(step)
        # print(step)
        recipe['directions'][iter] = step


    return recipe



if __name__ == "__main__":
    # Example usage
    recipe = {'ingredients': [{'amount': '1 3/4', 'unit': 'cups', 'name': 'flour', 'descriptor': 'all-purpose', 'preparation': 'divided'}, {'amount': '3/4', 'unit': 'cup', 'name': 'water', 'descriptor': 'warm', 'preparation': 'divided'}, {'amount': '1', 'unit': 'tablespoon', 'name': 'active  yeast', 'descriptor': 'dry', 'preparation': ''}, {'amount': '1', 'unit': 'teaspoon', 'name': 'sugar', 'descriptor': 'white', 'preparation': ''}, {'amount': '2', 'unit': 'tablespoons', 'name': 'sugar', 'descriptor': 'white', 'preparation': ''}, {'amount': '1', 'unit': 'tablespoon', 'name': 'oil', 'descriptor': 'vegetable', 'preparation': ''}, {'amount': '1/4', 'unit': 'teaspoon', 'name': 'salt', 'descriptor': '', 'preparation': ''}, {'amount': '1/2', 'unit': 'teaspoon', 'name': 'baking powder', 'descriptor': '', 'preparation': ''}], 'directions': {'Step 1': 'Gather all ingredients.', 'Step 2': 'Mix together 1/4 cup flour, 1/4 cup warm water, yeast, and 1 teaspoon sugar in a large bowl.', 'Step 3': 'Allow to sit for 30 minutes.', 'Step 4': 'Mix in remaining 1 1/2 cups flour, remaining 1/2 cup warm water, 2 tablespoons sugar, vegetable oil, and salt.', 'Step 5': 'Knead until dough is smooth and elastic.', 'Step 6': 'Transfer to a greased bowl, roll to coat with oil, and let sit until tripled in size, 2 1/2 to 3 hours.', 'Step 7': 'Punch down dough and spread out on a floured board.', 'Step 8': 'Sprinkle baking powder evenly on surface of dough; knead for 5 minutes.', 'Step 9': 'Divide dough in half; set aside one half in a covered bowl.', 'Step 10': 'Divide remaining half into 12 equal pieces.', 'Step 11': 'Shape each into a ball; transfer each ball to a small square of waxed paper with the smooth surface facing up.', 'Step 12': 'Repeat portioning and shaping with remaining dough half.', 'Step 13': 'Cover all 24 dough balls and let sit until doubled in size, about 30 minutes.', 'Step 14': 'Bring some water to a boil in a wok, then reduce heat to medium and keep water at a low boil.', 'Step 15': 'Place the steam plate on a small wire rack in the middle of the wok, leaving at least 2 inches of space between the plate and the wok.', 'Step 16': 'Working in batches, place buns on waxed paper squares onto the steam plate, leaving 1 to 2 inches between buns.', 'Step 17': 'Cover and steam buns for 15 minutes.', 'Step 18': "Carefully remove the lid, so condensation doesn't drip onto buns.", 'Step 19': 'Continue steaming remaining buns until all are cooked.'}, 'tools': ['wok', 'plate', 'bowl'], 'methods': ({'bake', 'cook', 'boil', 'heat', 'steam'}, {'double', 'face', 'divide', 'transfer', 'remove', 'shape', 'place', 'keep', 'leave', 'punch', 'mix', 'reduce', 'sit', 'remain', 'knead', 'continue', 'drip', 'gather', 'spread', 'let', 'triple', 'cover', 'wax', 'roll', 'bring', 'allow', 'set', 'repeat', 'work', 'sprinkle'})}
    # newrecipe = transform_recipe_healthiness(recipe, "unhealthy")
    # print(newrecipe)
    newrecipe = transform_recipe_healthiness(recipe, "healthy")
    print(newrecipe)
