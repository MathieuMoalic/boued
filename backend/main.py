from typing import List

from fastapi import Depends, FastAPI, HTTPException
from rapidfuzz import process
from sqlmodel import Session, SQLModel, create_engine, select

from backend.models import Item

database_url = "sqlite:///./test.db"
engine = create_engine(database_url, echo=True)

app = FastAPI()

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Create an item
@app.post("/items/", response_model=Item)
def create_item(item: Item, session: Session = Depends(get_session)):
    # Check if the item already exists
    existing_item = session.exec(select(Item).where(Item.name == item.name)).first()
    if existing_item:
        raise HTTPException(
            status_code=400, detail="Item with this name already exists."
        )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# Read all items
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items


# Read a single item by ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item


# Update an item
@app.put("/items/{item_id}", response_model=Item)
def update_item(
    item_id: int, item_update: Item, session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# Delete an item
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    session.delete(item)
    session.commit()
    return item


# Search items by name using fuzzy matching
@app.get("/search/", response_model=List[Item])
def search_items(query: str, limit: int = 10, session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    item_names = {item.name: item for item in items}
    # Perform fuzzy matching
    matches = process.extract(query, item_names.keys(), limit=limit)
    # Retrieve the matched items based on the names
    matched_items = [item_names[match[0]] for match in matches]
    return matched_items
