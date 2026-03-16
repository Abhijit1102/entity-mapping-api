import requests
from typing import List, Optional

from models.mappings import (
    VendorProductMappingCreate,
    VendorProductMappingUpdate,
    VendorProductMappingResponse,
)

BASE_URL = "http://127.0.0.1:8000/api/vendor-product-mappings/"


class VendorProductMappingAPIClient:

    def list_mappings(
        self,
        vendor_id: Optional[int] = None,
        product_id: Optional[int] = None,
    ) -> List[VendorProductMappingResponse]:
        params = {}
        if vendor_id is not None:
            params["vendor_id"] = vendor_id
        if product_id is not None:
            params["product_id"] = product_id

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        return [VendorProductMappingResponse(**m) for m in response.json()]

    def get_mapping(self, mapping_id: int) -> VendorProductMappingResponse:
        response = requests.get(f"{BASE_URL}{mapping_id}/")
        response.raise_for_status()

        return VendorProductMappingResponse(**response.json())

    def create_mapping(
        self, mapping: VendorProductMappingCreate
    ) -> VendorProductMappingResponse:
        response = requests.post(BASE_URL, json=mapping.model_dump())
        response.raise_for_status()

        return VendorProductMappingResponse(**response.json())

    def update_mapping(
        self, mapping_id: int, mapping: VendorProductMappingUpdate
    ) -> VendorProductMappingResponse:
        response = requests.put(
            f"{BASE_URL}{mapping_id}/",
            json=mapping.model_dump()
        )
        response.raise_for_status()

        return VendorProductMappingResponse(**response.json())

    def partial_update_mapping(
        self, mapping_id: int, mapping: VendorProductMappingUpdate
    ) -> VendorProductMappingResponse:
        response = requests.patch(
            f"{BASE_URL}{mapping_id}/",
            json=mapping.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return VendorProductMappingResponse(**response.json())

    def delete_mapping(self, mapping_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{mapping_id}/")
        response.raise_for_status()
