from pydantic import BaseModel
from typing import Optional


# ── Vendor ───────────────────────────────────

class VendorCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class VendorResponse(VendorCreate):
    id: int
    is_active: bool


# ── Product ──────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class ProductResponse(ProductCreate):
    id: int
    is_active: bool


# ── Course ───────────────────────────────────

class CourseCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class CourseResponse(CourseCreate):
    id: int
    is_active: bool


# ── Certification ─────────────────────────────

class CertificationCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class CertificationResponse(CertificationCreate):
    id: int
    is_active: bool
