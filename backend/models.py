from typing import Optional

from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    category: str = Field(index=True)
    is_active: bool = Field(default=False, index=True)
    notes: Optional[str] = Field(default=None)
    quantity: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)
