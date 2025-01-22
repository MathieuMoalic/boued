from typing import Any, Sequence

from sqlmodel import Session, select, update

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


def reorder_categories(
    session: Session, category_id: int, direction: str
) -> list[Category]:
    """
    Reorder a category by adjusting its 'order' field.

    Args:
        session (Session): The database session.
        category_id (int): The ID of the category to reorder.
        new_order (int): The new 'order' position.

    Raises:
        ValueError: If the category does not exist.
    """
    # Fetch the category
    category = session.get(Category, category_id)
    if not category:
        raise ValueError(f"Category with id={category_id} not found.")

    old_order = category.order
    new_order = old_order + 1 if direction == "down" else old_order - 1

    category.order = -1  # or some guaranteed-unique placeholder
    session.add(category)
    session.commit()

    # Shift orders for other categories in the range
    if old_order < new_order:
        # Move DOWN: Decrement orders in range (old_order, new_order]
        stmt = (
            update(Category)
            .where((Category.order > old_order) & (Category.order <= new_order))
            .values(order=Category.order - 1)  # subtract 1 from the column
        )
        session.exec(stmt)

    elif old_order > new_order:
        # Move UP: Increment orders in range [new_order, old_order)
        stmt = (
            update(Category)
            .where((Category.order >= new_order) & (Category.order < old_order))
            .values(order=Category.order + 1)  # add 1 to the column
        )
        session.exec(stmt)

    # Update the order of the current category
    category.order = new_order
    session.add(category)
    session.commit()

    # Optional: see final state
    all_categories = read_categories(session)
    return all_categories
