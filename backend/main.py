from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="Groceries API")
db = [[],[]]

with open("db.json", "w") as fp:
    json.dump({
        'active' : [],
        'inactive' : [],
        },fp)

with open("db.json","r") as f:
    db = json.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
def save():
    with open("db.json", "w") as fp:
        json.dump(db, fp)

@app.get("/api")
async def get_items():
    return db

@app.delete("/api/{item}")
async def delete_item(item: str):
    item = item.capitalize()
    if item in db['active']:
        db['active'].remove(item)
        db['inactive'].insert(0,item)
    save()
    return db

@app.post("/api/{item}")
async def add_item(item: str):
    item = item.capitalize()
    # if already in active, puts it at the top
    if item in db['active']:
        db['active'].remove(item)
        db['active'].insert(0,item)
    # else if in inactive, move it to active
    elif item in db['inactive']:
        db['inactive'].remove(item)
        db['active'].insert(0,item)
    else:
        db['active'].insert(0,item)
    save()
    return db
