def conversational_interface(recipe_data):
    current_step = 0
    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "show me the ingredients list":
            print("Ingredients:")
            for ingredient in recipe_data['ingredients']:
                print(f"- {ingredient}")

        elif user_input.startswith("go to the"):
            try:
                step_number = int(user_input.split()[-1]) - 1
                if 0 <= step_number < len(recipe_data['directions']):
                    current_step = step_number
                    print(f"Step {current_step + 1}: {recipe_data['directions'][current_step]}")
                else:
                    print("Invalid step number.")
            except ValueError:
                print("Please enter a valid step number.")

        elif user_input == "go back one step":
            if current_step > 0:
                current_step -= 1
                print(f"Step {current_step + 1}: {recipe_data['directions'][current_step]}")
            else:
                print("You are already at the first step.")

        elif user_input == "go to the next step":
            if current_step < len(recipe_data['directions']) - 1:
                current_step += 1
                print(f"Step {current_step + 1}: {recipe_data['directions'][current_step]}")
            else:
                print("You are already at the last step.")

        elif user_input == "repeat please":
            print(f"Step {current_step + 1}: {recipe_data['directions'][current_step]}")

        elif user_input.startswith("how much of"):
            ingredient_name = user_input.split("how much of ")[-1]
            for ingredient in recipe_data['ingredients']:
                if ingredient_name in ingredient["name"]:
                    amt = ingredient['amount']
                    unit = ingredient['unit']
                    name = ingredient['name']
                    
                    print(f"You need: {amt} {unit} of {name}")
                    break
            else:
                print(f"{ingredient_name} is not in the ingredients list.")

        elif user_input.startswith("what is"):
            query = user_input.replace(" ", "+")
            print(f"https://www.google.com/search?q={query}")

        elif user_input.startswith("how do i"):
            query = user_input.replace(" ", "+")
            print(f"https://www.youtube.com/results?search_query={query}")

        elif user_input == "how do i do that":
            # This requires conversation history to infer what "that" refers to.
            pass

        elif user_input == "exit":
            break

        else:
            print("I'm sorry, I didn't understand that.")

# Example usage
# conversational_interface(recipe_data)