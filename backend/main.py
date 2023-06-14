from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import meilisearch
from urllib.parse import unquote
import hashlib
from typing import TypedDict, Literal
import os
from fastapi.staticfiles import StaticFiles


MEILI_URL = os.environ["MEILI_URL"]
MEILI_KEY = os.environ["MEILI_KEY"]
DB_PATH = "/data/db.json"

Indices = Literal["Groceries", "Alcohol"]


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

meili = meilisearch.Client(MEILI_URL, MEILI_KEY)


def init_db():
    for index in meili.get_indexes()["results"]:
        index.delete()
    meili.create_index("Groceries", {"primaryKey": "id"})
    meili.create_index("Alcohol", {"primaryKey": "id"})
    db = {"active": {"Groceries": [], "Alcohol": []}, "Groceries": [], "Alcohol": []}
    with open(DB_PATH, "w") as fp:
        json.dump(db, fp)


if not os.path.exists(DB_PATH):
    init_db()


def get_id_from_name(string: str):
    return int(hashlib.md5(string.encode("utf-8")).hexdigest()[:5], 16)


with open(DB_PATH, "r") as f:
    db: Db = json.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def delete_item(category: Indices, item_name: str):
    item_name = unquote(item_name)
    if item_name in db["active"][category]:
        db["active"][category].remove(item_name)
    save()
    return db["active"]


@app.delete("/api/meili/{category}/{item_name}")
async def delete_meili_item(category: Indices, item_name: str):
    item_name = unquote(item_name)
    for item in db[category]:
        if item["name"] == item_name:
            db[category].remove(item)
            break
    meili.index(category).delete_document(get_id_from_name(item_name))
    return await delete_item(category, item_name)


@app.post("/api/{category}/{item_name}")
async def add_item(category: Indices, item_name: str):
    item_name = unquote(item_name)
    item_name = item_name.capitalize()
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
    meili.index(category).update_documents(
        [
            {
                "id": get_id_from_name(item_name),
                "name": item_name,
            }
        ]
    )
    save()
    return db["active"]


app.mount("/", StaticFiles(directory="static", html=True), name="static")
