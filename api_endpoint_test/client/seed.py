"""
Seed helper — creates master entities required by mapping tests
and cleans them up afterwards so the database stays empty.
"""
import requests
from models.entities import (
    VendorCreate, VendorResponse,
    ProductCreate, ProductResponse,
    CourseCreate, CourseResponse,
    CertificationCreate, CertificationResponse,
)

BASE = "http://127.0.0.1:8000/api"


def _post(url: str, payload: dict):
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def _delete(url: str, entity_id: int):
    response = requests.delete(f"{url}{entity_id}/")
    response.raise_for_status()


def create_vendor(name: str, code: str) -> VendorResponse:
    data = _post(f"{BASE}/vendors/", VendorCreate(name=name, code=code).model_dump())
    return VendorResponse(**data)


def create_product(name: str, code: str) -> ProductResponse:
    data = _post(f"{BASE}/products/", ProductCreate(name=name, code=code).model_dump())
    return ProductResponse(**data)


def create_course(name: str, code: str) -> CourseResponse:
    data = _post(f"{BASE}/courses/", CourseCreate(name=name, code=code).model_dump())
    return CourseResponse(**data)


def create_certification(name: str, code: str) -> CertificationResponse:
    data = _post(
        f"{BASE}/certifications/",
        CertificationCreate(name=name, code=code).model_dump()
    )
    return CertificationResponse(**data)


def delete_vendor(vendor_id: int):
    _delete(f"{BASE}/vendors/", vendor_id)


def delete_product(product_id: int):
    _delete(f"{BASE}/products/", product_id)


def delete_course(course_id: int):
    _delete(f"{BASE}/courses/", course_id)


def delete_certification(certification_id: int):
    _delete(f"{BASE}/certifications/", certification_id)
