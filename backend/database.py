from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./db.sqlite"
engine = create_engine(DATABASE_URL, echo=False)  # Disable SQL debug logs
SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency used to provide a DB session in FastAPI endpoints.
    """
    with Session(engine) as session:
        yield session
