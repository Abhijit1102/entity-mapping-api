from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    is_active: bool
