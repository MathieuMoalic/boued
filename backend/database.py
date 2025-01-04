# import os

from sqlmodel import Session, SQLModel, create_engine

# db_path = "./test.db"
# if os.path.exists(db_path):
#     os.remove(db_path)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=False)  # Disable SQL debug logs
SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency used to provide a DB session in FastAPI endpoints.
    """
    with Session(engine) as session:
        yield session


def init_db_with_data():
    """
    Initialize the database with some data.
    """
    from backend.models import Category, Item

    with Session(engine) as session:
        category_1 = Category(name="Category 1")
        category_2 = Category(name="Category 2")
        session.add(category_1)
        session.add(category_2)
        session.commit()

        item_1 = Item(name="Item 1", category_id=1)
        item_2 = Item(name="Item 2", category_id=2)
        session.add(item_1)
        session.add(item_2)
        session.commit()


# init_db_with_data()
