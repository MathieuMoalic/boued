from typing import Optional

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    is_active: bool = Field(default=False, index=True)
    notes: Optional[str] = Field(default=None)
    quantity: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    category_id: int = Field(default=None)
