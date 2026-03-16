import requests
from typing import List
from models.certification import (
    CertificationCreate,
    CertificationUpdate,
    CertificationResponse
)

BASE_URL = "http://127.0.0.1:8000/api/certifications/"


class CertificationAPIClient:

    def list_certifications(self) -> List[CertificationResponse]:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        certifications = response.json()
        return [CertificationResponse(**c) for c in certifications]


    def get_certification(self, certification_id: int) -> CertificationResponse:
        response = requests.get(f"{BASE_URL}{certification_id}/")
        response.raise_for_status()

        return CertificationResponse(**response.json())


    def create_certification(self, certification: CertificationCreate) -> CertificationResponse:
        response = requests.post(BASE_URL, json=certification.model_dump())
        response.raise_for_status()

        return CertificationResponse(**response.json())


    def update_certification(self, certification_id: int, certification: CertificationUpdate) -> CertificationResponse:
        response = requests.put(
            f"{BASE_URL}{certification_id}/",
            json=certification.model_dump()
        )
        response.raise_for_status()

        return CertificationResponse(**response.json())


    def partial_update_certification(self, certification_id: int, certification: CertificationUpdate) -> CertificationResponse:
        response = requests.patch(
            f"{BASE_URL}{certification_id}/",
            json=certification.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return CertificationResponse(**response.json())


    def delete_certification(self, certification_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{certification_id}/")
        response.raise_for_status()
