from typing import Any, Sequence

from sqlmodel import Session, select

from backend.models import Category, Item


def read_categories(session: Session) -> Sequence[Category]:
    """Return all categories, ordered by the 'order' field."""
    categories = session.exec(select(Category).order_by(Category.order)).all()
    return categories


def create_category(session: Session, data: dict[str, Any]) -> Category:
    """
    Create a new category with the next available 'order' value.
    Raises:
        ValueError: If a category with this name already exists,
                    or if 'name' is missing/invalid in data.
    """
    # Check if "name" is provided
    if "name" not in data or not data["name"]:
        raise ValueError("Category 'name' is required.")

    # Check if category already exists
    existing_category = session.exec(
        select(Category).where(Category.name == data["name"])
    ).first()
    if existing_category:
        raise ValueError("Category already exists.")

    # Assign the next available 'order' value if not provided
    if "order" not in data or data["order"] is None:
        max_order = session.exec(
            select(Category.order).order_by(Category.order.desc())
        ).first()
        data["order"] = (max_order or 0) + 1

    category = Category(**data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def update_category(
    session: Session, category_id: int, data: dict[str, Any]
) -> Category:
    """
    Update an existing category by ID.
    Raises:
        ValueError: If the category does not exist,
                    if the 'name' is already taken by another category,
                    or if the 'order' conflicts.
    """
    # Make sure the category exists
    category = session.get(Category, category_id)
    if not category:
        raise ValueError("Category not found.")

    # Handle name update and ensure uniqueness
    if "name" in data and data["name"] is not None:
        if data["name"] != category.name:
            existing_category = session.exec(
                select(Category).where(Category.name == data["name"])
            ).first()
            if existing_category and existing_category.id != category_id:
                raise ValueError("Another category already has this name.")

    # Handle order update and ensure uniqueness
    if "order" in data and data["order"] is not None:
        if data["order"] != category.order:
            conflicting_category = session.exec(
                select(Category).where(Category.order == data["order"])
            ).first()
            if conflicting_category and conflicting_category.id != category_id:
                raise ValueError(f"Another category already has order {data['order']}.")

    # Update fields
    for key, value in data.items():
        setattr(category, key, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def delete_category(session: Session, category_id: int) -> Category:
    """
    Delete a category by ID.
    Re-assign items belonging to this category to category_id=1
    (if that is your 'Uncategorized' category).
    Raises:
        ValueError: If the category does not exist.
    """
    category = session.get(Category, category_id)
    if not category:
        raise ValueError("Category not found.")

    # Find all items referencing this category
    items = session.exec(select(Item).where(Item.category_id == category_id)).all()
    if items:
        # Assign items to the 'Uncategorized' category (ID=1)
        for item in items:
            item.category_id = 1
            session.add(item)
        session.commit()

    session.delete(category)
    session.commit()
    return category


def reorder_categories(session: Session, category_id: int, new_order: int) -> None:
    """
    Reorder a category by adjusting the 'order' field.
    Raises:
        ValueError: If the category does not exist or the new order conflicts.
    """
    category = session.get(Category, category_id)
    if not category:
        raise ValueError("Category not found.")

    # Shift orders to accommodate the new order
    if category.order < new_order:
        # Move down: Decrement orders in the range (old_order, new_order]
        session.exec(
            select(Category).where(
                (Category.order > category.order) & (Category.order <= new_order)
            )
        ).update({"order": Category.order - 1})
    elif category.order > new_order:
        # Move up: Increment orders in the range [new_order, old_order)
        session.exec(
            select(Category).where(
                (Category.order >= new_order) & (Category.order < category.order)
            )
        ).update({"order": Category.order + 1})

    # Update the order of the current category
    category.order = new_order
    session.add(category)
    session.commit()
