from directions import fetch_recipe_page
from datafetch import parse_recipe
from parserhelper import find_ingredients_in_string
from parserhelper import answer_cooking_question
import string
import re

user_session = {}

def get_step(delta):
    if user_session.get("last_action") == "recipe_selected":
        user_session["current_step"] += delta
        steps = user_session.get("steps", {})
        step_number = f"Step {user_session['current_step']}"

        if step_number in steps:
            return f"{step_number}: {steps[step_number]}"
        else:
            user_session["current_step"] -= delta
            return "No more steps."
    else:
        return "Please provide a valid AllRecipes URL first."

def main():
    global user_session
    print("Welcome to the Recipe Assistant! Please specify an AllRecipes URL.")
    while True:
        user_message = input("\n> ").lower()

        if "allrecipes.com" in user_message:
            url = user_message.strip('<>')
            print("Fetching recipe...")
            html_content = fetch_recipe_page(url)
            parsed_recipe = parse_recipe(html_content)

            user_session = {
                "ingredients": parsed_recipe['ingredients'],
                "tools": parsed_recipe['tools'],
                "steps": parsed_recipe['directions'],
                "methods": parsed_recipe['methods'],
                "current_step": 0,
                "last_action": "recipe_selected"
            }
            print("Recipe loaded. What would you like to do?")
            print("* List ingredients")
            print("* List tools")
            print("* Go over recipe steps")

        elif "ingredients" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                ingredients = user_session.get("ingredients", [])
                formatted_ingredients = [
                    f"{item['amount']} {item['unit']} {item['name']}" for item in ingredients
                ]
                print("Here are the ingredients:")
                print("\n".join(formatted_ingredients))
            else:
                print("Please provide a valid AllRecipes URL first.")
        
        elif "tools" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                tools = user_session.get("tools", [])
                print("Here are the tools:")
                print("\n".join(tools))
            else:
                print("Please provide a valid AllRecipes URL first.")

        elif "list" in user_message and "recipe steps" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                steps = user_session.get("steps", {})
                for step, value in steps.items():
                    print(f"{step}: {value}")
            else:
                print("Please provide a valid AllRecipes URL first.")

        elif "recipe step" in user_message:
            print(get_step(1))

        elif "next" in user_message and "step" in user_message:
            print(get_step(1))

        elif "repeat" in user_message and "step" in user_message:
            print(get_step(0))

        elif ("previous" in user_message or "back" in user_message) and "step" in user_message:
            print(get_step(-1))

        elif " to step " in user_message:
            step = int(user_message.split()[-1])
            if user_session.get("last_action") == "recipe_selected":
                steps = user_session.get("steps", {})
                step_number = f"Step {step}"
                if step_number in steps:
                    user_session["current_step"] = step
                    print(f"{step_number}: {steps[step_number]}")
                else:
                    print(f"{step_number} does not exist.")
            else:
                print("Please provide a valid AllRecipes URL first.")

        elif "how long do i" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                current_step = user_session['steps'][f"Step {user_session['current_step']}"]
                print(answer_cooking_question(current_step, user_message))
            else:
                print("Please provide a valid AllRecipes URL first.")

        elif "how much" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                pattern = r"how much\s+(.*?)(?:\s+(do|should|is)|$)"
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    ingr_text = match.group(1)
                    print(ingr_text)
                    for ingredient in user_session['ingredients']:
                        if ingr_text in ingredient["name"]:
                            amt = ingredient['amount']
                            unit = ingredient['unit']
                    current_step = user_session['steps']['Step ' + str(user_session["current_step"])]
                    for part in current_step.split(','):
                        if ingr_text in part:
                            search_text = part.split(ingr_text)[0].split()
                            isDigit = False
                            i = len(search_text) - 1

                            while i >= 0:
                                if all(char.isdigit() or char in string.punctuation for char in search_text[i]):
                                    isDigit = True
                                    break
                                else:
                                    i -= 1

                            if not isDigit:
                                print(f"You need: {amt} {unit} of {ingr_text} for this step.")
                            else:
                                unit2 = search_text[i + 1]
                                amount = search_text[i]
                                if i - 1 >= 0 and search_text[i-1].isdigit():
                                    amount = search_text[i-1] + " " + search_text[i]
                                print(f"You need: {amount} {unit2} of {ingr_text} for this step.")
                    if ingr_text not in current_step:
                        print(f"{ingr_text} not used in this step")
                else:
                    print("Unrecognized command.")
            else:
                print("Please provide a valid AllRecipes URL first.")
        

        elif "how do i do that" in user_message or "how do you do that" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                current_step = user_session['steps'][f"Step {user_session['current_step']}"]
                no_punctuation = current_step.translate(str.maketrans('', '', string.punctuation)).split()

                ingredients = find_ingredients_in_string(user_session['ingredients'], current_step)
                if not ingredients:
                    print("Google Search: https://www.google.com/search?q=how+to+"+'+'.join(no_punctuation))
                else:
                    filtered_words = []
                    i = 0
                    while i < len(no_punctuation):
                        if no_punctuation[i].isdigit():
                            while i < len(no_punctuation) and no_punctuation[i].isdigit():
                                i += 1
                            i += 1
                        else:
                            filtered_words.append(no_punctuation[i])
                            i += 1
                    print("Google Search: https://www.google.com/search?q=how+to+"+'+'.join(filtered_words))
            else:
                print("Please provide a valid AllRecipes URL first.")

        elif user_message.startswith("what is") or user_message.startswith("how to") or user_message.startswith("how do i") or "instead" in user_message:
            if user_session.get("last_action") == "recipe_selected":
                print(f"Google Search: https://www.google.com/search?q={'+'.join(user_message.split())}")
            else:
                print("Please provide a valid AllRecipes URL first.")

        elif user_message in ["exit", "quit"]:
            print("Goodbye!")
            break

        else:
            if user_session.get("last_action") == "recipe_selected":
                print("Unrecognized command. Please try again.")
            else:
                print("Please specify an AllRecipes URL.")

if __name__ == "__main__":
    main()
