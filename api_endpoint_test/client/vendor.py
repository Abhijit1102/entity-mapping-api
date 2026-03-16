import requests
from typing import List
from models.vendor import VendorCreate, VendorUpdate, VendorResponse

BASE_URL = "http://127.0.0.1:8000/api/vendors/"


class VendorAPIClient:

    def list_vendors(self) -> List[VendorResponse]:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        vendors = response.json()
        return [VendorResponse(**v) for v in vendors]

    def get_vendor(self, vendor_id: int) -> VendorResponse:
        response = requests.get(f"{BASE_URL}{vendor_id}/")
        response.raise_for_status()

        return VendorResponse(**response.json())

    def create_vendor(self, vendor: VendorCreate) -> VendorResponse:
        response = requests.post(BASE_URL, json=vendor.model_dump())
        response.raise_for_status()

        return VendorResponse(**response.json())

    def update_vendor(self, vendor_id: int, vendor: VendorUpdate) -> VendorResponse:
        response = requests.put(
            f"{BASE_URL}{vendor_id}/",
            json=vendor.model_dump()
        )
        response.raise_for_status()

        return VendorResponse(**response.json())

    def partial_update_vendor(self, vendor_id: int, vendor: VendorUpdate) -> VendorResponse:
        response = requests.patch(
            f"{BASE_URL}{vendor_id}/",
            json=vendor.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return VendorResponse(**response.json())

    def delete_vendor(self, vendor_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{vendor_id}/")
        response.raise_for_status()
