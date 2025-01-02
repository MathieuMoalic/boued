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
