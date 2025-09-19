
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
from fastapi.responses import HTMLResponse


app = FastAPI(
    title="Recipe API",
    description="A simple FastAPI app using JSON as a database, demonstrating GET, POST, PUT, DELETE and HTML response for recipes.",
    version="1.0.0"
)


# Always resolve data.json relative to this file
DATA_FILE = Path(__file__).parent / "data.json"


def read_data():
    """Read JSON file and return its contents."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error reading JSON file:", e)
        return {"recipes": []}


def write_data(data):
    """Write data back to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


class Recipe(BaseModel):
    id: int
    title: str
    ingredients: list[str]
    instructions: str
    cooking_time: int  # in minutes
    difficulty: str
    image_url: str = None


@app.get("/recipes", response_model=list[Recipe])
def list_recipes():
    """Return all recipes from data.json."""
    data = read_data()
    return data["recipes"]


@app.get("/recipes/{id}", response_model=Recipe)
def get_recipe(id: int):
    """Return a single recipe by its id."""
    data = read_data()
    for recipe in data["recipes"]:
        if recipe["id"] == id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")


@app.post("/recipes", response_model=Recipe)
def add_recipe(recipe: Recipe):
    """Add a new recipe to the JSON file."""
    data = read_data()
    if any(r["id"] == recipe.id for r in data["recipes"]):
        raise HTTPException(status_code=400, detail="Recipe id already exists")
    data["recipes"].append(recipe.dict())
    write_data(data)
    return recipe


@app.put("/recipes/{id}", response_model=Recipe)
def update_recipe(id: int, recipe: Recipe):
    """Update an existing recipe identified by its id."""
    data = read_data()
    for idx, r in enumerate(data["recipes"]):
        if r["id"] == id:
            data["recipes"][idx] = recipe.dict()
            write_data(data)
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")


@app.delete("/recipes/{id}")
def delete_recipe(id: int):
    """Delete a recipe by its id."""
    data = read_data()
    for idx, r in enumerate(data["recipes"]):
        if r["id"] == id:
            deleted = data["recipes"].pop(idx)
            write_data(data)
            return {"deleted": deleted}
    raise HTTPException(status_code=404, detail="Recipe not found")


@app.get("/recipes/{id}/image", response_class=HTMLResponse)
def show_recipe_image(id: int):
        """
        Show an HTML page with the recipe image embedded.
        This demonstrates returning HTML instead of JSON.
        """
        data = read_data()
        for recipe in data["recipes"]:
                if recipe["id"] == id and recipe.get("image_url"):
                        ingredients_html = "<ul>" + "".join(f"<li>{ing}</li>" for ing in recipe["ingredients"]) + "</ul>"
                        return f"""
                        <html>
                            <head><title>{recipe['title']}</title></head>
                            <body style='text-align:center; font-family:sans-serif;'>
                                <h1>{recipe['title']} (ID: {recipe['id']})</h1>
                                <p><b>Difficulty:</b> {recipe['difficulty']} | <b>Cooking Time:</b> {recipe['cooking_time']} min</p>
                                <h2>Ingredients</h2>
                                {ingredients_html}
                                <h2>Instructions</h2>
                                <p>{recipe['instructions']}</p>
                                <img src="{recipe['image_url']}" alt="recipe image" style="max-width:80%; height:auto; margin-top:20px;" />
                            </body>
                        </html>
                        """
        raise HTTPException(status_code=404, detail="Recipe not found or no image URL")
