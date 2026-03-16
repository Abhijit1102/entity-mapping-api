import requests
from typing import List

from models.entities import CertificationCreate, CertificationResponse

BASE_URL = "http://127.0.0.1:8000/api/certifications/"


class CertificationAPIClient:

    def list_certifications(self) -> List[CertificationResponse]:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return [CertificationResponse(**c) for c in response.json()]

    def get_certification(self, cert_id: int) -> CertificationResponse:
        response = requests.get(f"{BASE_URL}{cert_id}/")
        response.raise_for_status()
        return CertificationResponse(**response.json())

    def create_certification(self, cert: CertificationCreate) -> CertificationResponse:
        response = requests.post(BASE_URL, json=cert.model_dump())
        response.raise_for_status()
        return CertificationResponse(**response.json())

    def update_certification(self, cert_id: int, cert: CertificationCreate) -> CertificationResponse:
        response = requests.put(f"{BASE_URL}{cert_id}/", json=cert.model_dump())
        response.raise_for_status()
        return CertificationResponse(**response.json())

    def partial_update_certification(self, cert_id: int, data: dict) -> CertificationResponse:
        response = requests.patch(f"{BASE_URL}{cert_id}/", json=data)
        response.raise_for_status()
        return CertificationResponse(**response.json())

    def delete_certification(self, cert_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{cert_id}/")
        response.raise_for_status()
