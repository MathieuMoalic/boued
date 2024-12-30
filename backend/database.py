import os

from sqlmodel import Session, SQLModel, create_engine

db_path = "./test.db"
if os.path.exists(db_path):
    os.remove(db_path)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=False)  # Disable SQL debug logs
SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency used to provide a DB session in FastAPI endpoints.
    """
    with Session(engine) as session:
        yield session


def init_db_data():
    from backend.models import Category, Item

    with Session(engine) as session:
        # Create categories
        categories = [
            Category(name="Other"),
            Category(name="Fruit"),
            Category(name="Vegetable"),
            Category(name="Vegan"),
            Category(name="Canned"),
            Category(name="Beverages"),
        ]
        session.add_all(categories)
        session.commit()

        # Create items
        items = [
            Item(
                name="Laptop",
                category_id=1,
                quantity=10,
                is_active=True,
                unit="pcs",
                notes="For office use",
            ),
            Item(
                name="Apples",
                category_id=2,
                quantity=50,
                unit="kg",
                notes="Fresh apples",
            ),
            Item(
                name="T-Shirt",
                category_id=3,
                quantity=100,
                unit="pcs",
                notes="Cotton T-Shirts",
            ),
        ]
        session.add_all(items)
        session.commit()


init_db_data()
