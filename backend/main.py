import json
from typing import Optional

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from rapidfuzz import process
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    category: str = Field(index=True)
    is_active: bool = Field(default=False, index=True)
    notes: Optional[str] = Field(default=None)
    quantity: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)


# Database setup
database_url = "sqlite:///./test.db"
engine = create_engine(database_url, echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for message in websocket.iter_text():
        try:
            # Parse message (assumes JSON format)
            data = json.loads(message)  # Parse JSON from text
            action = data.get("action")
            payload = data.get("payload")

            # Perform actions based on the "action" type
            if action == "create":
                result = create_item(payload)
                await websocket.send_json({"status": "success", "data": result})
            elif action == "read_all":
                result = read_items()
                await websocket.send_json({"status": "success", "data": result})
            elif action == "read_one":
                item_id = payload.get("id")
                result = read_item(item_id)
                await websocket.send_json({"status": "success", "data": result})
            elif action == "update":
                item_id = payload.get("id")
                update_data = payload.get("data")
                result = update_item(item_id, update_data)
                await websocket.send_json({"status": "success", "data": result})
            elif action == "delete":
                item_id = payload.get("id")
                result = delete_item(item_id)
                await websocket.send_json({"status": "success", "data": result})
            elif action == "search":
                query = payload.get("query")
                limit = payload.get("limit", 10)
                result = search_items(query, limit)
                await websocket.send_json({"status": "success", "data": result})
            else:
                await websocket.send_json(
                    {"status": "error", "message": "Invalid action"}
                )
        except Exception as e:
            await websocket.send_json({"status": "error", "message": str(e)})


def create_item(data: dict):
    with Session(engine) as session:
        item = Item(**data)
        existing_item = session.exec(select(Item).where(Item.name == item.name)).first()
        if existing_item:
            raise ValueError("Item with this name already exists.")
        session.add(item)
        session.commit()
        session.refresh(item)
        return item.model_dump()


def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return [item.model_dump() for item in items]


def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise ValueError("Item not found.")
        return item.model_dump()


def update_item(item_id: int, update_data: dict):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise ValueError("Item not found.")
        for key, value in update_data.items():
            setattr(item, key, value)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item.model_dump()


def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise ValueError("Item not found.")
        session.delete(item)
        session.commit()
        return item.model_dump()


def search_items(query: str, limit: int = 10):
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        item_names = {item.name: item for item in items}
        matches = process.extract(query, item_names.keys(), limit=limit)
        return [item_names[match[0]].model_dump() for match in matches]


app.mount("/", StaticFiles(directory="./static", html=True), name="static")
