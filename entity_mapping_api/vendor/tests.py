from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vendor

class VendorAPITestCase(APITestCase):

    def setUp(self):
        """Create initial vendor"""
        self.vendor = Vendor.objects.create(
            name="Acme Corp",
            code="ACME001",
            description="Technology vendor"
        )

        self.list_url = "/api/vendors/"
        self.detail_url = f"/api/vendors/{self.vendor.id}/"

    # GET /api/vendors/
    def test_list_vendors(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # POST /api/vendors/
    def test_create_vendor(self):
        data = {
            "name": "Google",
            "code": "GOOG001",
            "description": "Tech vendor"
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    # POST invalid vendor
    def test_create_vendor_invalid(self):
        data = {
            "name": ""
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # GET /api/vendors/{id}/
    def test_retrieve_vendor(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Acme Corp")

    # GET vendor not found
    def test_retrieve_vendor_not_found(self):
        response = self.client.get("/api/vendors/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PUT /api/vendors/{id}/
    def test_full_update_vendor(self):
        data = {
            "name": "Updated Vendor",
            "code": "ACME001",
            "description": "Updated description"
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, "Updated Vendor")

    # PATCH /api/vendors/{id}/
    def test_partial_update_vendor(self):
        data = {
            "description": "Partially updated description"
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.description, "Partially updated description")

    # PATCH invalid field
    def test_partial_update_invalid(self):
        data = {
            "name": ""
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE /api/vendors/{id}/
    def test_delete_vendor(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    # DELETE vendor not found
    def test_delete_vendor_not_found(self):
        response = self.client.delete("/api/vendors/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
