from pydantic import BaseModel
from typing import Optional


class VendorBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class VendorResponse(VendorBase):
    id: int
    is_active: bool
