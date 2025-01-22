from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.crud.categories import (
    create_category,
    delete_category,
    read_categories,
    reorder_categories,
    update_category,
)
from backend.database import get_session
from backend.jwt import get_current_user
from backend.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate
from backend.websocket import ws

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", operation_id="categoryCreate")
async def create_category_endpoint(
    category_data: CategoryCreate, session: Session = Depends(get_session)
):
    """
    Create a new category.
    """
    category = create_category(session, category_data.model_dump())
    await ws.send_message(
        action="create", obj_type="category", data=category.model_dump()
    )


@router.get("", response_model=List[CategoryRead], operation_id="categoryreadAll")
async def read_categories_endpoint(session: Session = Depends(get_session)):
    """
    Read all categories.
    """
    categories = read_categories(session)
    return categories


@router.put("/{category_id}", operation_id="categoryUpdate")
async def update_category_endpoint(
    category_id: int,
    update_data: CategoryUpdate,
    session: Session = Depends(get_session),
):
    """
    Update an existing category by ID.
    """
    category = update_category(
        session, category_id, update_data.model_dump(exclude_unset=True)
    )
    await ws.send_message(
        action="update", obj_type="category", data=category.model_dump()
    )


@router.put(
    "/reorder/{category_id}",
    operation_id="categoryReorder",
)
async def reorder_category_endpoint(
    category_id: int,
    direction: str,
    session: Session = Depends(get_session),
):
    if direction not in ["up", "down"]:
        raise ValueError("Invalid direction")
    """
    Reorder a category by ID.
    """
    categories = reorder_categories(session, category_id, direction)
    await ws.send_message(
        action="reorder", obj_type="category", data=[c.model_dump() for c in categories]
    )


@router.delete("/{category_id}", operation_id="categoryDelete")
async def delete_category_endpoint(
    category_id: int, session: Session = Depends(get_session)
):
    """
    Delete an category by ID.
    """
    category = delete_category(session, category_id)
    await ws.send_message(
        action="delete", obj_type="category", data=category.model_dump()
    )
