import requests
from typing import List, Optional

from models.mappings import (
    ProductCourseMappingCreate,
    ProductCourseMappingUpdate,
    ProductCourseMappingResponse,
)

BASE_URL = "http://127.0.0.1:8000/api/product-course-mappings/"


class ProductCourseMappingAPIClient:

    def list_mappings(
        self,
        product_id: Optional[int] = None,
        course_id: Optional[int] = None,
    ) -> List[ProductCourseMappingResponse]:
        params = {}
        if product_id is not None:
            params["product_id"] = product_id
        if course_id is not None:
            params["course_id"] = course_id

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        return [ProductCourseMappingResponse(**m) for m in response.json()]

    def get_mapping(self, mapping_id: int) -> ProductCourseMappingResponse:
        response = requests.get(f"{BASE_URL}{mapping_id}/")
        response.raise_for_status()

        return ProductCourseMappingResponse(**response.json())

    def create_mapping(
        self, mapping: ProductCourseMappingCreate
    ) -> ProductCourseMappingResponse:
        response = requests.post(BASE_URL, json=mapping.model_dump())
        response.raise_for_status()

        return ProductCourseMappingResponse(**response.json())

    def update_mapping(
        self, mapping_id: int, mapping: ProductCourseMappingUpdate
    ) -> ProductCourseMappingResponse:
        response = requests.put(
            f"{BASE_URL}{mapping_id}/",
            json=mapping.model_dump()
        )
        response.raise_for_status()

        return ProductCourseMappingResponse(**response.json())

    def partial_update_mapping(
        self, mapping_id: int, mapping: ProductCourseMappingUpdate
    ) -> ProductCourseMappingResponse:
        response = requests.patch(
            f"{BASE_URL}{mapping_id}/",
            json=mapping.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return ProductCourseMappingResponse(**response.json())

    def delete_mapping(self, mapping_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{mapping_id}/")
        response.raise_for_status()
