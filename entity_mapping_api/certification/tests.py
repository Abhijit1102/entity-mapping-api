from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Certification


class CertificationAPITestCase(APITestCase):

    def setUp(self):
        """Create initial certification"""

        self.certification = Certification.objects.create(
            name="AWS Certified Developer",
            code="AWS001",
            description="Amazon certification",
            is_active=True
        )

        self.list_url = reverse("certification-list")
        self.detail_url = reverse("certification-detail", args=[self.certification.id])


    # GET list
    def test_list_certifications(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # POST create
    def test_create_certification(self):

        data = {
            "name": "Google Cloud Professional",
            "code": "GCP001",
            "description": "Google cloud certification",
            "is_active": True
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Certification.objects.count(), 2)


    # POST invalid
    def test_create_certification_invalid(self):

        data = {
            "name": "",
            "code": ""
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # GET detail
    def test_retrieve_certification(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "AWS Certified Developer")


    # GET not found
    def test_retrieve_certification_not_found(self):

        url = reverse("certification-detail", args=[999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PUT update
    def test_full_update_certification(self):

        data = {
            "name": "AWS Certified Dev Updated",
            "code": "AWS001",
            "description": "Updated description",
            "is_active": True
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.certification.refresh_from_db()
        self.assertEqual(self.certification.name, "AWS Certified Dev Updated")


    # PATCH update
    def test_partial_update_certification(self):

        data = {
            "description": "Partially updated description"
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.certification.refresh_from_db()
        self.assertEqual(self.certification.description, "Partially updated description")


    # PATCH invalid
    def test_partial_update_invalid(self):

        data = {"name": ""}

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # DELETE
    def test_delete_certification(self):

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Certification.objects.count(), 0)


    # DELETE not found
    def test_delete_certification_not_found(self):

        url = reverse("certification-detail", args=[999])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
