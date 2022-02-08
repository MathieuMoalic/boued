from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tinydb import TinyDB, Query

app = FastAPI(title="Groceries API")
db = TinyDB("./db.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_items():
    return db.all()


@app.delete("/{item_id}")
async def delete_item(item_id: int):
    out = db.search(Query().id == item_id)
    if len(out) == 1:
        db.remove(Query().id == item_id)
    return db.all()


@app.post("/{item_name}")
async def add_item(item_name: str):
    for item_id in range(256):
        if len(db.search(Query().id == item_id)) == 0:
            db.insert({"id": item_id, "name": item_name})
            return db.all()
