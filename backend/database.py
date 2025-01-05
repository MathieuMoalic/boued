from sqlmodel import Session, SQLModel, create_engine, select

from backend.crud.categories import create_category
from backend.crud.items import create_item
from backend.models import Category

DATABASE_URL = "sqlite:////data/db1.sqlite"
engine = create_engine(DATABASE_URL, echo=False)  # Disable SQL debug logs
SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency used to provide a DB session in FastAPI endpoints.
    """
    with Session(engine) as session:
        yield session


# check the number of categories
with Session(engine) as session:
    categories = session.exec(select(Category)).all()
    if len(categories) == 0:
        print("Creating base categories.")
        with Session(engine) as session:
            category = create_category(session, {"name": "Other"})
            category = create_category(session, {"name": "Fruits"})
            category = create_category(session, {"name": "Vegetables"})
            category = create_category(session, {"name": "Bakery"})
            category = create_category(session, {"name": "Drinks"})
            category = create_category(session, {"name": "Alcohol"})
            category = create_category(session, {"name": "Non-food"})
        print("Creating base items.")
        with Session(engine) as session:
            item = create_item(session, {"name": "Apple", "category_id": 2})
            item = create_item(session, {"name": "Banana", "category_id": 2})
            item = create_item(session, {"name": "Carrot", "category_id": 3})
            item = create_item(session, {"name": "Potato", "category_id": 3})
            item = create_item(session, {"name": "Bread", "category_id": 4})
            item = create_item(session, {"name": "Milk", "category_id": 5})
            item = create_item(session, {"name": "Beer", "category_id": 6})
            item = create_item(session, {"name": "Soap", "category_id": 7})
            item = create_item(session, {"name": "Orange", "category_id": 2})
            item = create_item(session, {"name": "Pear", "category_id": 2})
            item = create_item(session, {"name": "Cucumber", "category_id": 3})
            item = create_item(session, {"name": "Tomato", "category_id": 3})
            item = create_item(session, {"name": "White wine", "category_id": 6})
            item = create_item(session, {"name": "Red wine", "category_id": 6})
            item = create_item(session, {"name": "Toilet paper", "category_id": 7})
            item = create_item(session, {"name": "Shampoo", "category_id": 7})
            item = create_item(session, {"name": "Conditioner", "category_id": 7})
            item = create_item(session, {"name": "Tofu", "category_id": 3})
            item = create_item(session, {"name": "Soy milk", "category_id": 5})
            item = create_item(session, {"name": "Vegan cheese", "category_id": 5})
            item = create_item(session, {"name": "Vegan sausage", "category_id": 5})
            item = create_item(session, {"name": "Vegan burger", "category_id": 5})
