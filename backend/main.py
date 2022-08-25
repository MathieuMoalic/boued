from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tinydb import TinyDB, Query

app = FastAPI(title="Groceries API")
db = TinyDB(f"./db.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def flip(list1:list):
    return sorted(list1,key=lambda x:x["id"],reverse=True)

@app.get("/api")
async def get_items():
    return flip(db.all())


@app.delete("/api/{item_id}")
async def delete_item(item_id: int):
    db.remove(Query().id == item_id)
    return flip(db.all())


@app.post("/api/{item_name}")
async def add_item(item_name: str):
    for item_id in range(256):
        if len(db.search(Query().id == item_id)) == 0:
            db.insert({"id": item_id, "name": item_name})
            return flip(db.all())
