import hashlib
import json
import os
import time
from pathlib import Path
from typing import Literal, TypedDict
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from rapidfuzz import fuzz, process

DEV = "DEV" in os.environ

DB_PATH = Path("/data/db.json")

Category = Literal["Groceries", "Alcohol"]


class Item(TypedDict):
    name: str
    id: int


class Active(TypedDict):
    Groceries: list[str]
    Alcohol: list[str]


class Db(TypedDict):
    active: Active
    Groceries: list[Item]
    Alcohol: list[Item]


app = FastAPI(title="Groceries API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

time.sleep(2)  # Reduced sleep time as no external service to wait for

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    db = {"active": {"Groceries": [], "Alcohol": []}, "Groceries": [], "Alcohol": []}
    with open(DB_PATH, "w") as fp:
        json.dump(db, fp)
    print("Database created.")


if not DB_PATH.exists():
    print("Database not found, creating an empty one.")
    init_db()

with open(DB_PATH, "r") as f:
    db: Db = json.load(f)


def get_id_from_name(string: str):
    return int(hashlib.md5(string.encode("utf-8")).hexdigest()[:5], 16)


def save():
    with open(DB_PATH, "w") as fp:
        json.dump(db, fp)


@app.get("/api")
async def get_items():
    return db["active"]


@app.get("/api/key")
async def get_key():
    return db["active"]


@app.delete("/api/{category}/{item_name}")
async def delete_item(category: Category, item_name: str):
    item_name = unquote(item_name).capitalize()
    if item_name in db["active"][category]:
        db["active"][category].remove(item_name)
        db[category] = [item for item in db[category] if item["name"] != item_name]
        save()
        return db["active"]
    else:
        raise HTTPException(status_code=404, detail="Item not found in active list.")


@app.post("/api/{category}/{item_name}")
async def add_item(category: Category, item_name: str):
    item_name = unquote(item_name).capitalize()
    if item_name in db["active"][category]:
        db["active"][category].remove(item_name)
    db["active"][category].insert(0, item_name)
    db[category] = [item for item in db[category] if item.get("name") != item_name]
    db[category].insert(
        0,
        {
            "id": get_id_from_name(item_name),
            "name": item_name,
        },
    )
    save()
    return db["active"]


@app.get("/api/search/{category}/{search_input}")
async def get_search(category: Category, search_input: str):
    # Extract the list of item names from the category
    items = [item["name"] for item in db[category]]
    # Use RapidFuzz to find the best matches
    matches = process.extract(search_input, items, scorer=fuzz.WRatio, limit=8)
    # Filter out matches with low similarity scores (optional)
    filtered_matches = [match[0] for match in matches if match[1] >= 60]
    return filtered_matches


if not DEV:
    # In production, FastAPI will serve the compiled Svelte bundle
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
