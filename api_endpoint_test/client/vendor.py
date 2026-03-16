import requests
from typing import List

from models.entities import VendorCreate, VendorResponse

BASE_URL = "http://127.0.0.1:8000/api/vendors/"


class VendorAPIClient:

    def list_vendors(self) -> List[VendorResponse]:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return [VendorResponse(**v) for v in response.json()]

    def get_vendor(self, vendor_id: int) -> VendorResponse:
        response = requests.get(f"{BASE_URL}{vendor_id}/")
        response.raise_for_status()
        return VendorResponse(**response.json())

    def create_vendor(self, vendor: VendorCreate) -> VendorResponse:
        response = requests.post(BASE_URL, json=vendor.model_dump())
        response.raise_for_status()
        return VendorResponse(**response.json())

    def update_vendor(self, vendor_id: int, vendor: VendorCreate) -> VendorResponse:
        response = requests.put(f"{BASE_URL}{vendor_id}/", json=vendor.model_dump())
        response.raise_for_status()
        return VendorResponse(**response.json())

    def partial_update_vendor(self, vendor_id: int, data: dict) -> VendorResponse:
        response = requests.patch(f"{BASE_URL}{vendor_id}/", json=data)
        response.raise_for_status()
        return VendorResponse(**response.json())

    def delete_vendor(self, vendor_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{vendor_id}/")
        response.raise_for_status()
