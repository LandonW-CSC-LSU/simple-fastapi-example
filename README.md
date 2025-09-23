Recipe API

Simple FastAPI app that stores recipes in a data.json file and allows viewing of that data.

Setup
	1.	Install with pip install fastapi.
	2.	Create a data.json file next to main.py with { "recipes": [] } if it does not already exist.
	3.	Run with fastapi dev main.py.
API will be at http://127.0.0.1:8000 and docs at http://127.0.0.1:8000/docs.

Endpoints

GET /recipes – list all recipes
GET /recipes/{id} – get one recipe
POST /recipes – add a recipe
PUT /recipes/{id} – update a recipe
DELETE /recipes/{id} – delete a recipe
GET /recipes/{id}/page – HTML page for a recipe

Example request:

Fetch recipe with id 1 using curl:
curl http://127.0.0.1:8000/recipes/1

Group Members:
Felix Schafer - 89-334-1528
