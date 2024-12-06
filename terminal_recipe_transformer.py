from directions import fetch_recipe_page
from datafetch import parse_recipe
from multiplier import multiply_ingredients
from dairyfree import transform_recipe_to_lactose_free
from to_vegetarian import to_veg_transformation
from to_nonvegetarian import to_nonveg_transformation
from healthy import transform_recipe_healthiness
from to_indian import to_indian
import copy

def write_recipe_to_txt(recipe_data, file_path, transformation):
    human_readable = []

    human_readable.append(f"Transformation: {transformation}\n")

    human_readable.append("Ingredients:\n")
    for ingredient in recipe_data.get('ingredients', []):
        if ingredient.get('descriptor', ''):
            line = f"- {ingredient.get('amount', '')} {ingredient.get('unit', '')} {ingredient.get('descriptor', '')} {ingredient.get('name', '')} {ingredient.get('preparation', '')}".strip()
        else:
            line = f"- {ingredient.get('amount', '')} {ingredient.get('unit', '')} {ingredient.get('name', '')} {ingredient.get('preparation', '')}".strip()
        human_readable.append(line)

    human_readable.append("\nDirections:\n")
    for step, instruction in recipe_data.get('directions', {}).items():
        human_readable.append(f"{step}: {instruction}")

    human_readable.append("\nTools:\n" + ", ".join(recipe_data.get('tools', [])))

    human_readable.append("\nMethods:\n" + ", ".join(list(recipe_data.get('methods', [])[0])))

    with open(file_path, "w") as file:
        file.write("\n".join(human_readable))
    
def main():
    print("Welcome to the Recipe Transformer! Please specify an AllRecipes URL.")
    user_message = input("\n> ").lower()

    url = user_message.strip('<>')
    print("Fetching recipe...")
    html_content = fetch_recipe_page(url)
    parsed_recipe = parse_recipe(html_content)

    print("Recipe loaded! ")
    print("Select the transformation you would like to do on this recipe:")
    print("(1) to vegetarian") 
    print("(2) to non-vegetarian")
    print("(3) to healthy")
    print("(4) to unhealthy")
    print("(5) to Indian-style cuisine")
    print("(6) half recipe amount")
    print("(7) double recipe amount")
    print("(8) to lactose free") 

    # demo
    # https://www.allrecipes.com/chicken-carbonara-pasta-bake-recipe-7969899
    # (1) veg, (3) healthy, (8) lactose free
    # pranav, keene, cheryl

    # https://www.allrecipes.com/recipe/8890/general-tsaos-chicken/
    # (3) healthy, (4) unhealthy, (7) double
    # keene, keene, cheryl

    # https://www.allrecipes.com/recipe/240559/traditional-gyros/
    # (5) indian, (1) veg, (6) half
    # pranav, pranav, cheryl

    # https://www.allrecipes.com/green-bean-mac-and-cheese-recipe-8753390
    # (2) non veg
    # pranav

    user_choice = input("\n> ").lower()
    if user_choice == "1":
        write_recipe_to_txt(to_veg_transformation(copy.deepcopy(parsed_recipe)), "to_vegetarian_recipe_transformation.txt", "to vegetarian")
        print("Transformed recipe written to to_vegetarian_recipe_transformation.txt")
        write_recipe_to_txt(parsed_recipe, "to_vegetarian_original_recipe.txt", "to vegetarian (before transformation)")
        print("Original recipe written to to_vegetarian_original_recipe.txt")
    elif user_choice == "2":
        write_recipe_to_txt(to_nonveg_transformation(copy.deepcopy(parsed_recipe)), "to_nonvegetarian_recipe_transformation.txt", "to non-vegetarian")
        print("Transformed recipe written to to_nonvegetarian_recipe_transformation.txt")
        write_recipe_to_txt(parsed_recipe, "to_nonvegetarian_original_recipe.txt", "to non-vegetarian (before transformation)")
        print("Original recipe written to to_nonvegetarian_original_recipe.txt")
    elif user_choice == "3":
        write_recipe_to_txt(transform_recipe_healthiness(copy.deepcopy(parsed_recipe), "healthy"), "to_healthy_recipe_transformation.txt", "to healthy")
        print("Transformed recipe written to to_healthy_recipe_transformation.txt")
        write_recipe_to_txt(parsed_recipe, "to_healthy_original_recipe.txt", "to healthy (before transformation)")
        print("Original recipe written to to_healthy_original_recipe.txt")
    elif user_choice == "4":
        write_recipe_to_txt(transform_recipe_healthiness(copy.deepcopy(parsed_recipe), "unhealthy"), "to_unhealthy_recipe_transformation.txt", "to unhealthy")
        print("Transformed recipe written to to_unhealthy_recipe_transformation.txt")
        write_recipe_to_txt(parsed_recipe, "to_unhealthy_original_recipe.txt", "to unhealthy (before transformation)")
        print("Original recipe written to to_unhealthy_original_recipe.txt")
    elif user_choice == "5":
        write_recipe_to_txt(to_indian(copy.deepcopy(parsed_recipe)), "to_indian_recipe_transformation.txt", "to Indian style cuisine")
        print("Transformed recipe written to to_indian_recipe_transformation.txt")
        write_recipe_to_txt(parsed_recipe, "to_indian_original_recipe.txt", "to Indian style cuisine (before transformation)")
        print("Original recipe written to to_indian_original_recipe.txt")
    elif user_choice == "6":
        write_recipe_to_txt(multiply_ingredients(copy.deepcopy(parsed_recipe), 0.5), "half_recipe_amount_transformation.txt", "half recipe amount")
        print("Transformed recipe written to half_recipe_amount_transformation.txt")
        write_recipe_to_txt(multiply_ingredients(copy.deepcopy(parsed_recipe), 1), "half_amount_original_recipe.txt", "half recipe amount (before transformation)")
        print("Original recipe written to half_amount_original_recipe.txt")
    elif user_choice == "7":
        write_recipe_to_txt(multiply_ingredients(copy.deepcopy(parsed_recipe), 2), "double_recipe_amount_transformation.txt", "double recipe amount")
        print("Transformed recipe written to double_recipe_amount_transformation.txt")
        write_recipe_to_txt(multiply_ingredients(copy.deepcopy(parsed_recipe), 1), "double_amount_original_recipe.txt", "double recipe amount (before transformation)")
        print("Original recipe written to double_amount_original_recipe.txt")
    elif user_choice == "8":
        write_recipe_to_txt(transform_recipe_to_lactose_free(copy.deepcopy(parsed_recipe)), "to_lactose_free_recipe_transformation.txt", "to lactose free")
        print("Transformed recipe written to to_lactose_free_recipe_transformation.txt")
        write_recipe_to_txt(parsed_recipe, "to_lactose_free_original_recipe.txt", "to lactose free (before transformation)")
        print("Original recipe written to to_lactose_free_original_recipe.txt")
        


if __name__ == "__main__":
    main()
