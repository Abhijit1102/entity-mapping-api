from rest_framework.test import APITestCase
from rest_framework import status

from course.models import Course
from certification.models import Certification
from .models import CourseCertificationMapping


class CourseCertificationMappingAPITestCase(APITestCase):

    def setUp(self):
        """Create initial data"""

        self.course = Course.objects.create(
            name="Cloud Fundamentals",
            code="CF001",
            description="Intro to cloud computing"
        )

        self.certification = Certification.objects.create(
            name="AWS Certified Cloud Practitioner",
            code="AWS-CCP",
            description="Entry-level AWS certification"
        )

        self.mapping = CourseCertificationMapping.objects.create(
            course=self.course,
            certification=self.certification,
            is_primary=True
        )

        self.list_url = "/api/course-certification-mappings/"
        self.detail_url = f"/api/course-certification-mappings/{self.mapping.id}/"


    # GET /api/course-certification-mappings/
    def test_list_mappings(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with course filter
    def test_filter_by_course(self):
        response = self.client.get(f"{self.list_url}?course_id={self.course.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with certification filter
    def test_filter_by_certification(self):
        response = self.client.get(f"{self.list_url}?certification_id={self.certification.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with non-matching filter returns empty
    def test_filter_returns_empty_for_unknown_id(self):
        response = self.client.get(f"{self.list_url}?course_id=999")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    # POST /api/course-certification-mappings/
    def test_create_mapping(self):

        new_certification = Certification.objects.create(
            name="Azure Fundamentals",
            code="AZ-900"
        )

        data = {
            "course": self.course.id,
            "certification": new_certification.id,
            "is_primary": False
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseCertificationMapping.objects.count(), 2)


    # POST duplicate mapping
    def test_create_duplicate_mapping(self):

        data = {
            "course": self.course.id,
            "certification": self.certification.id,
            "is_primary": False
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # POST second primary mapping for same course
    def test_create_second_primary_mapping(self):

        new_certification = Certification.objects.create(
            name="GCP Associate",
            code="GCP-ACE"
        )

        data = {
            "course": self.course.id,
            "certification": new_certification.id,
            "is_primary": True
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # POST invalid mapping (missing fields)
    def test_create_mapping_invalid(self):

        data = {
            "course": "",
            "certification": ""
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # GET /api/course-certification-mappings/{id}/
    def test_retrieve_mapping(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course"], self.course.id)
        self.assertEqual(response.data["certification"], self.certification.id)


    # GET mapping not found
    def test_retrieve_mapping_not_found(self):

        response = self.client.get("/api/course-certification-mappings/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PUT /api/course-certification-mappings/{id}/
    def test_full_update_mapping(self):

        new_certification = Certification.objects.create(
            name="Google Professional Data Engineer",
            code="GCP-PDE"
        )

        data = {
            "course": self.course.id,
            "certification": new_certification.id,
            "is_primary": False
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.mapping.refresh_from_db()
        self.assertEqual(self.mapping.certification.id, new_certification.id)


    # PUT mapping not found
    def test_full_update_mapping_not_found(self):

        data = {
            "course": self.course.id,
            "certification": self.certification.id,
            "is_primary": False
        }

        response = self.client.put(
            "/api/course-certification-mappings/999/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PATCH /api/course-certification-mappings/{id}/
    def test_partial_update_mapping(self):

        data = {
            "is_primary": False
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.mapping.refresh_from_db()
        self.assertEqual(self.mapping.is_primary, False)


    # PATCH invalid field
    def test_partial_update_invalid(self):

        data = {
            "course": ""
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # PATCH mapping not found
    def test_partial_update_not_found(self):

        response = self.client.patch(
            "/api/course-certification-mappings/999/",
            {"is_primary": False},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # DELETE /api/course-certification-mappings/{id}/
    def test_delete_mapping(self):

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CourseCertificationMapping.objects.count(), 0)


    # DELETE mapping not found
    def test_delete_mapping_not_found(self):

        response = self.client.delete("/api/course-certification-mappings/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
