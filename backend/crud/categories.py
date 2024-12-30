from typing import Any, Sequence

from sqlmodel import Session, select

from backend.models import Category


def read_categories(session: Session) -> Sequence[Category]:
    categories = session.exec(select(Category)).all()
    return categories


def create_category(session: Session, data: dict[str, Any]) -> Category:
    # check if category already exists
    category = session.exec(
        select(Category).where(Category.name == data["name"])
    ).first()
    if category:
        raise ValueError("Category already exists.")
    category = Category(**data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def update_category(
    session: Session, category_id: int, update_data: dict[str, Any]
) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise ValueError("Category not found.")
    for key, value in update_data.items():
        setattr(category, key, value)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def delete_category(session: Session, category_id: int) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise ValueError("Category not found.")
    session.delete(category)
    session.commit()
    return category
