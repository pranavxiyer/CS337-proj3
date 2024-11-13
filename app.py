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
