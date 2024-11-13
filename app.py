from slack_bolt import App
from dotenv import load_dotenv
from directions import fetch_recipe_page 
from datafetch import parse_recipe
import os

# https://cs337-proj2.onrender.com/slack/events

load_dotenv()
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

user_sessions = {}    

def get_step(user_id, delta):
    if user_sessions.get(user_id, {}).get("last_action") == "recipe_selected":
        user_sessions[user_id]["current_step"] += delta
        steps = user_sessions[user_id].get("steps", [])
        step_number = 'Step ' + str(user_sessions.get(user_id)["current_step"])

        if step_number in steps:
            return f"{step_number}: {steps[step_number]}"
        else:
            return "No more steps."
    else:
        return "Please provide a recipe URL first."

@app.event("message")
def handle_dm_messages(event, say):
    if event.get("channel_type") == "im":
        user_id = event.get("user")
        user_message = str(event.get("text")).lower()

        if "https://www.allrecipes.com" in user_message:
            url = user_message.strip('<>')
            html_content = fetch_recipe_page(url)
            parsed_recipe = parse_recipe(html_content)

            if user_id not in user_sessions:
                user_sessions[user_id] = {
                    "ingredients": parsed_recipe['ingredients'],
                    "tools": parsed_recipe['tools'],
                    "steps": parsed_recipe['directions'],
                    "current_step": 0,
                    "last_action": "recipe_selected"
                }

            say(text="What do you want to do?")
            say(text="[1] List ingredients")
            say(text="[2] List tools")
            say(text="[3] Go over recipe steps")
        
        elif "list" in user_message and "ingredients" in user_message:
            if user_sessions.get(user_id, {}).get("last_action") == "recipe_selected":
                ingredients = user_sessions[user_id].get("ingredients", [])

                formatted_ingredients = [f"{item['amount']} {item['unit']} {item['name']}" for item in ingredients]

                say(text="Here are the ingredients:\n" + "\n".join(formatted_ingredients))
            else:
                say(text="Please provide a recipe URL first.")
            
        
        elif "list" in user_message and "tools" in user_message:
            if user_sessions.get(user_id, {}).get("last_action") == "recipe_selected":
                tools = user_sessions[user_id].get("tools", [])
                say(text="Here are the tools:\n" + "\n".join(tools))
            else:
                say(text="Please provide a recipe URL first.")

        elif "recipe steps" in user_message:
            say(text=get_step(user_id, 1))

        elif "next" in user_message and "step" in user_message:
            say(text=get_step(user_id, 1))

        elif "repeat" in user_message and "step" in user_message:
            say(text=get_step(user_id, 0))

        elif ("previous" in user_message or "back" in user_message) and "step" in user_message:
            say(text=get_step(user_id, -1))

        
        elif "how much" in user_message:
            ingredient_name = user_message.split("how much of ")[-1]
            for ingredient in parsed_recipe['ingredients']:
                if ingredient_name in ingredient["name"]:
                    amt = ingredient['amount']
                    unit = ingredient['unit']
                    ingr_name = ingredient['name']
                    current_step = steps['Step ' + str(user_sessions.get(user_id)["current_step"])]
                    if ingredient_name in current_step:
                        ing_words = ingredient_name.split()
                        step_words = current_step.split()
                        
                        if ing_words[0] in step_words:
                            ind = step_words.index(ing_words[0])
                            inplace = True
                            for i in range(ing_words):
                                if step_words[ind + i] != ing_words[i]:
                                    ind = False
                                    break
                            if inplace:
                                unit2 = step_words[ind - 1]
                                amount = step_words[ind - 2]
                                amount_ind = ind - 3
                                while any(chr.isdigit() for chr in step_words[amount_ind]):
                                    amount.append(step_words[amount_ind])
                                    amount_ind -= 1
                                amount = amount.reverse()
                                amount = " ".join(amount)    
                                print(f"For this step specifically, you need {amt} {unit2} of {ingr_name}")
                    print(f"You need: {amt} {unit} of {ingr_name}")

        elif user_message.startswith("go to step "):
            step = int(user_message.split()[-1])
            if user_sessions.get(user_id, {}).get("last_action") == "recipe_selected":
                user_sessions[user_id]["current_step"] = step
                steps = user_sessions[user_id].get("steps", [])
                step_number = 'Step ' + str(user_sessions.get(user_id)["current_step"])

                if step_number in steps:
                    say(text=f"{step_number}: {steps[step_number]}")
                else:
                    say(text=step_number + " does not exist.")
            else:
                return say(text="Please provide a recipe URL first.")
            
        elif user_message.startswith("what is") or user_message.startswith("how to") or user_message.startswith("how do i"):
            say(text="https://www.google.com/search?q="+'+'.join(user_message.split()))
        
        else:
            if user_id not in user_sessions:
                say(text="Please specify an AllRecipes URL.")
            else:
                say(text="Unrecognized command.")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
