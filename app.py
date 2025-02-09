import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

load_dotenv()

app = FastAPI(
    title="Drink API",
    summary="A sample API to fetch drinks, ingredients, and glasses from MongoDB."
)

client = MongoClient(os.getenv("MONGODB_URL"))
db = client.get_database(os.getenv("DB_NAME"))

# 🥤 Get all drinks or search by name dynamically
@app.get("/drinks")
async def get_drinks(name: str = Query(None, description="Search for drinks containing this name")):
    collection = db.get_collection("drinks")

    if name:
        # Search for drinks that CONTAIN the name anywhere in the string
        documents = list(collection.find({"name": {"$regex": name, "$options": "i"}}))
    else:
        documents = list(collection.find())

    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string

    if name and not documents:
        raise HTTPException(status_code=404, detail=f"No drinks found containing '{name}'")

    return JSONResponse(content=documents)


# 🥃 Get a single drink by exact name
@app.get("/drinks/{name}")
async def get_drink_by_name(name: str):
    collection = db.get_collection("drinks")
    document = collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

    if not document:
        raise HTTPException(status_code=404, detail=f"Drink '{name}' not found")

    document["_id"] = str(document["_id"])  # Convert ObjectId to string
    return JSONResponse(content=document)

# 🍋 Get all ingredients or search by name
@app.get("/ingredients")
async def get_ingredients(name: str = Query(None, description="Search for ingredients containing this name")):
    collection = db.get_collection("ingredients")

    if name:
        documents = list(collection.find({"name": {"$regex": name, "$options": "i"}}))
    else:
        documents = list(collection.find())

    for doc in documents:
        doc["_id"] = str(doc["_id"])  

    if name and not documents:
        raise HTTPException(status_code=404, detail=f"No ingredients found containing '{name}'")

    return JSONResponse(content=documents)

# 🍹 Get a single ingredient by exact name
@app.get("/ingredients/{name}")
async def get_ingredient_by_name(name: str):
    collection = db.get_collection("ingredients")
    document = collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

    if not document:
        raise HTTPException(status_code=404, detail=f"Ingredient '{name}' not found")

    document["_id"] = str(document["_id"])
    return JSONResponse(content=document)

# 🥂 Get all glasses or search by name
@app.get("/glasses")
async def get_glasses(name: str = Query(None, description="Search for glasses containing this name")):
    collection = db.get_collection("glasses")

    if name:
        documents = list(collection.find({"name": {"$regex": name, "$options": "i"}}))
    else:
        documents = list(collection.find())

    for doc in documents:
        doc["_id"] = str(doc["_id"])  

    if name and not documents:
        raise HTTPException(status_code=404, detail=f"No glasses found containing '{name}'")

    return JSONResponse(content=documents)

# 🏺 Get a single glass by exact name
@app.get("/glasses/{name}")
async def get_glass_by_name(name: str):
    collection = db.get_collection("glasses")
    document = collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

    if not document:
        raise HTTPException(status_code=404, detail=f"Glass '{name}' not found")

    document["_id"] = str(document["_id"])
    return JSONResponse(content=document)
