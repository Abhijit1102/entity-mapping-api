from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendorProductMappingBase(BaseModel):
    vendor: int
    product: int
    is_primary: Optional[bool] = False


class VendorProductMappingCreate(VendorProductMappingBase):
    pass


class VendorProductMappingUpdate(BaseModel):
    vendor: Optional[int] = None
    product: Optional[int] = None
    is_primary: Optional[bool] = None


class VendorProductMappingResponse(VendorProductMappingBase):
    id: int
    created_at: datetime


# ─────────────────────────────────────────────


class ProductCourseMappingBase(BaseModel):
    product: int
    course: int
    is_primary: Optional[bool] = False


class ProductCourseMappingCreate(ProductCourseMappingBase):
    pass


class ProductCourseMappingUpdate(BaseModel):
    product: Optional[int] = None
    course: Optional[int] = None
    is_primary: Optional[bool] = None


class ProductCourseMappingResponse(ProductCourseMappingBase):
    id: int
    created_at: datetime


# ─────────────────────────────────────────────


class CourseCertificationMappingBase(BaseModel):
    course: int
    certification: int
    is_primary: Optional[bool] = False


class CourseCertificationMappingCreate(CourseCertificationMappingBase):
    pass


class CourseCertificationMappingUpdate(BaseModel):
    course: Optional[int] = None
    certification: Optional[int] = None
    is_primary: Optional[bool] = None


class CourseCertificationMappingResponse(CourseCertificationMappingBase):
    id: int
    created_at: datetime
