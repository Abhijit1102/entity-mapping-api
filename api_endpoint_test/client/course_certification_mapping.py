import requests
from typing import List, Optional

from models.mappings import (
    CourseCertificationMappingCreate,
    CourseCertificationMappingUpdate,
    CourseCertificationMappingResponse,
)

BASE_URL = "http://127.0.0.1:8000/api/course-certification-mappings/"


class CourseCertificationMappingAPIClient:

    def list_mappings(
        self,
        course_id: Optional[int] = None,
        certification_id: Optional[int] = None,
    ) -> List[CourseCertificationMappingResponse]:
        params = {}
        if course_id is not None:
            params["course_id"] = course_id
        if certification_id is not None:
            params["certification_id"] = certification_id

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        return [CourseCertificationMappingResponse(**m) for m in response.json()]

    def get_mapping(self, mapping_id: int) -> CourseCertificationMappingResponse:
        response = requests.get(f"{BASE_URL}{mapping_id}/")
        response.raise_for_status()

        return CourseCertificationMappingResponse(**response.json())

    def create_mapping(
        self, mapping: CourseCertificationMappingCreate
    ) -> CourseCertificationMappingResponse:
        response = requests.post(BASE_URL, json=mapping.model_dump())
        response.raise_for_status()

        return CourseCertificationMappingResponse(**response.json())

    def update_mapping(
        self, mapping_id: int, mapping: CourseCertificationMappingUpdate
    ) -> CourseCertificationMappingResponse:
        response = requests.put(
            f"{BASE_URL}{mapping_id}/",
            json=mapping.model_dump()
        )
        response.raise_for_status()

        return CourseCertificationMappingResponse(**response.json())

    def partial_update_mapping(
        self, mapping_id: int, mapping: CourseCertificationMappingUpdate
    ) -> CourseCertificationMappingResponse:
        response = requests.patch(
            f"{BASE_URL}{mapping_id}/",
            json=mapping.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return CourseCertificationMappingResponse(**response.json())

    def delete_mapping(self, mapping_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{mapping_id}/")
        response.raise_for_status()
