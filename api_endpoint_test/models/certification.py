from pydantic import BaseModel
from typing import Optional


class CertificationBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class CertificationResponse(CertificationBase):
    id: int
    is_active: bool
