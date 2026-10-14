from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from pprint import pprint
import os

class Ingredient(BaseModel):
    """
    Model for a recipe ingredient.
    """
    amount: Optional[float] = Field(description="Quantity of the ingredient")
    unit: Optional[str] = Field(description="Unit of measurement, such as cup, tbsp, or oz")
    name: str = Field(description="Name of the ingredient")

class Recipe(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    title: str = Field(description="Name of the recipe")
    ingredients: List[Ingredient] = Field(description="List of ingredients needed for the recipe")
    instructions: List[str] = Field(description="Step-by-step instructions to prepare the recipe")

def get_recipe_from_text(recipe_text: str) -> Recipe:
    """
    Convert recipe text into a structured Recipe object using OpenAI.
    """
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # Make the API call
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"Convert this recipe into the specified format:\n\n{recipe_text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Recipe
        )
    )
    
    return response.parsed

# Example usage
if __name__ == "__main__":
    # Read recipe text from file
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    recipe_path = os.path.join(script_dir, "mac_and_cheese_recipe.txt")
    with open(recipe_path, "r") as file:
        recipe_text = file.read()

    # Get structured recipe
    recipe = get_recipe_from_text(recipe_text)
    
    # Print results
    pprint(recipe)
    # pprint(recipe) # to see the whole object