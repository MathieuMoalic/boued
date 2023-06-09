from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="Groceries API")

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

@app.delete("/api/{category}/{item_name}")
async def delete_item(category: str, item_name: str):
    for item in db:
        if item['name'] == item_name and item['category'] == category:
            db.insert(0, db.pop(db.index(item)))
            db[0]['active'] = False
    save()
    return db

@app.post("/api/{category}/{item_name}")
async def add_item(category: str, item_name: str):
    item_name = item_name.capitalize()
    # if already in active, puts it at the top
    found = False
    for item in db:
        if item['name'] == item_name and item['category'] == category:
            db.insert(0, db.pop(db.index(item)))
            db[0]['active'] = True
            found = True
    if not found :
        db.insert(0,{'name':item_name,'active':True,'category':category,'emoji':''})
    save()
    return db
