from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.corpus import verbnet
import string

def is_cooking_utensil(word):
    
    tagged_word = pos_tag([word])
    if tagged_word[0][1] != 'NN':
        return False
    
    
    synsets = wn.synsets(word)
    for synset in synsets:
        if 'artifact' in synset.lexname() or 'instrumentality' in synset.lexname():
            # Check if any of the word's definitions contain cooking-related terms
            definition = synset.definition().lower()
            cooking_terms = ['cook', 'food', 'kitchen', 'utensil', 'culinary', 'mix']
            if any(term in definition for term in cooking_terms):
                return True
    
    return False


def extract_tools(directions):
    translator = str.maketrans('', '', string.punctuation)
    # Use the translate method to remove punctuation

    words = []
    for sent in directions:
        sent = sent.translate(translator)
        words.extend(sent.split())
    artifacts = []
    for word in words:
        # for word in sent:
        if is_cooking_utensil(word):
            artifacts.append(word.lower())
    return list(set(artifacts))



if __name__ == "__main__":

    directions = [
        "Heat a wok over medium heat .",
        "Use a grater to shred the cheese .",
        "Whisk the eggs in a bowl .",
        "Cook the vegetables in a pan .",
        "Preheat the oven to 350 degrees F. "
    ]
    print(extract_tools(directions))