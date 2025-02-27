import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

load_dotenv()

app = FastAPI(
    title="Drink API",
    summary="An API to fetch drinks, ingredients, and glasses from MongoDB.",
)

client = MongoClient(os.getenv("MONGODB_URL"))
db = client.get_database(os.getenv("DB_NAME"))


# Fetch all collections once and return
def fetch_all_data():
    drink_collection = db.get_collection("drinks")
    ingredient_collection = db.get_collection("ingredients")
    glass_collection = db.get_collection("glasses")

    # Fetch all documents without limiting fields
    drink_documents = list(drink_collection.find())  # No projection (fetch all fields)
    ingredient_documents = list(
        ingredient_collection.find()
    )  # No projection (fetch all fields)
    glass_documents = list(glass_collection.find())  # No projection (fetch all fields)

    return drink_documents, ingredient_documents, glass_documents


# Helper function to convert ObjectId to string
def convert_objectid_to_str(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def update_entity_with_drink_images(doc, drink_dict):
    # Convert ObjectId to string for the drink
    doc = convert_objectid_to_str(doc)

    # Add images to ingredients
    if doc.get("drinks"):
        doc["drinks"] = [
            {"name": drink, "image": drink_dict[drink]["image"]}
            for drink in doc["drinks"]
        ]


# Function to add image to ingredients
def add_image_to_ingredient(ingredient, ingredient_dict):
    ingredient_name = ingredient.get("name")
    if ingredient_name:
        ingredient_data = ingredient_dict.get(ingredient_name)
        if ingredient_data:
            ingredient["image"] = ingredient_data.get("image")


# Function to add image to glass
def add_image_to_glass(glass, glass_dict):
    glass_name = glass.get("name")
    if glass_name:
        glass_data = glass_dict.get(glass_name)
        if glass_data:
            glass["image"] = glass_data.get("image")


# Function to update drink with ingredient and glass images
def update_drink_with_images(doc, ingredient_dict, glass_dict):
    # Convert ObjectId to string for the drink
    doc = convert_objectid_to_str(doc)

    # Add images to ingredients
    if doc.get("ingredients"):
        for ingredient in doc["ingredients"]:
            add_image_to_ingredient(ingredient, ingredient_dict)

    # Add image to glass
    if doc.get("glass"):
        glass = doc.get("glass")
        if glass:
            add_image_to_glass(glass, glass_dict)

    return doc


# 🥤 Get all drinks or search by name dynamically
@app.get("/drinks")
async def get_drinks(
    name: str = Query(None, description="Search for drinks containing this name")
):
    drinks, ingredients, glasses = fetch_all_data()

    # Convert the ingredient and glass documents into dictionaries for quick lookup
    ingredient_dict = {ingredient["name"]: ingredient for ingredient in ingredients}
    glass_dict = {glass["name"]: glass for glass in glasses}

    # Filter drinks by name if provided
    if name:
        drinks = [doc for doc in drinks if name.lower() in doc.get("name", "").lower()]

    # Update the drinks documents
    updated_drinks = [
        update_drink_with_images(doc, ingredient_dict, glass_dict) for doc in drinks
    ]

    # If no drinks were found after filtering, raise 404 error
    if not updated_drinks:
        raise HTTPException(
            status_code=404, detail=f"No drinks found containing '{name}'"
        )

    return JSONResponse(content=updated_drinks)


# 🥃 Get a single drink by exact name
@app.get("/drinks/{name}")
async def get_drink_by_name(name: str):
    drinks, ingredients, glasses = fetch_all_data()

    # Convert the ingredient and glass documents into dictionaries for quick lookup
    ingredient_dict = {ingredient["name"]: ingredient for ingredient in ingredients}
    glass_dict = {glass["name"]: glass for glass in glasses}

    # Find the drink by name in the path parameter
    drink = next(
        (doc for doc in drinks if name.lower() == doc.get("name", "").lower()), None
    )

    # If drink not found, raise 404 error
    if not drink:
        raise HTTPException(
            status_code=404, detail=f"Drink with name '{name}' not found"
        )

    # Update the drink document with images
    updated_drink = update_drink_with_images(drink, ingredient_dict, glass_dict)

    return JSONResponse(content=updated_drink)


# 🍋 Get all ingredients or search by name
@app.get("/ingredients")
async def get_ingredients(
    name: str = Query(None, description="Search for ingredients containing this name")
):
    drinks, ingredients, _ = fetch_all_data()
    drinks_dict = {drink["name"]: drink for drink in drinks}

    # Filter ingredients by name if provided
    if name:
        ingredients = [
            doc for doc in ingredients if name.lower() in doc.get("name", "").lower()
        ]

    # Update the drinks documents
    for doc in ingredients:
        update_entity_with_drink_images(doc, drinks_dict)

    if name and not ingredients:
        raise HTTPException(
            status_code=404, detail=f"No ingredients found containing '{name}'"
        )

    return JSONResponse(content=ingredients)


# 🍹 Get a single ingredient by exact name
@app.get("/ingredients/{name}")
async def get_ingredient_by_name(name: str):
    drinks, ingredients, _ = fetch_all_data()
    drinks_dict = {drink["name"]: drink for drink in drinks}

    # Find the ingredient by name in the path parameter
    ingredient = next(
        (doc for doc in ingredients if name.lower() == doc.get("name", "").lower()),
        None,
    )

    update_entity_with_drink_images(ingredient, drinks_dict)

    if not ingredient:
        raise HTTPException(status_code=404, detail=f"Ingredient '{name}' not found")

    ingredient["_id"] = str(ingredient["_id"])
    return JSONResponse(content=ingredient)


# 🥂 Get all glasses or search by name
@app.get("/glasses")
async def get_glasses(
    name: str = Query(None, description="Search for glasses containing this name")
):
    drinks, _, glasses = fetch_all_data()
    drinks_dict = {drink["name"]: drink for drink in drinks}

    # Filter glasses by name if provided
    if name:
        glasses = [
            doc for doc in glasses if name.lower() in doc.get("name", "").lower()
        ]

    # Update the glasses documents
    for doc in glasses:
        update_entity_with_drink_images(doc, drinks_dict)

    if name and not glasses:
        raise HTTPException(
            status_code=404, detail=f"No glasses found containing '{name}'"
        )

    return JSONResponse(content=glasses)


# 🏺 Get a single glass by exact name
@app.get("/glasses/{name}")
async def get_glass_by_name(name: str):
    drinks, _, glasses = fetch_all_data()
    drinks_dict = {drink["name"]: drink for drink in drinks}

    # Find the glass by name in the path parameter
    glass = next(
        (doc for doc in glasses if name.lower() == doc.get("name", "").lower()),
        None,
    )

    update_entity_with_drink_images(glass, drinks_dict)

    if not glass:
        raise HTTPException(status_code=404, detail=f"Ingredient '{name}' not found")

    glass["_id"] = str(glass["_id"])
    return JSONResponse(content=glass)
