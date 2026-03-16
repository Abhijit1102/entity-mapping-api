from rest_framework.test import APITestCase
from rest_framework import status

from vendor.models import Vendor
from product.models import Product
from .models import VendorProductMapping


class VendorProductMappingAPITestCase(APITestCase):

    def setUp(self):
        """Create initial data"""

        self.vendor = Vendor.objects.create(
            name="Acme Corp",
            code="ACME001",
            description="Tech vendor"
        )

        self.product = Product.objects.create(
            name="Laptop",
            code="LAP001",
            description="Electronics product"
        )

        self.mapping = VendorProductMapping.objects.create(
            vendor=self.vendor,
            product=self.product,
            is_primary=True
        )

        self.list_url = "/api/vendor-product-mappings/"
        self.detail_url = f"/api/vendor-product-mappings/{self.mapping.id}/"


    # GET /api/vendor-product-mappings/
    def test_list_mappings(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with vendor filter
    def test_filter_by_vendor(self):
        response = self.client.get(f"{self.list_url}?vendor_id={self.vendor.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with product filter
    def test_filter_by_product(self):
        response = self.client.get(f"{self.list_url}?product_id={self.product.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # POST /api/vendor-product-mappings/
    def test_create_mapping(self):

        new_product = Product.objects.create(
            name="Mouse",
            code="MOU001"
        )

        data = {
            "vendor": self.vendor.id,
            "product": new_product.id,
            "is_primary": False
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorProductMapping.objects.count(), 2)


    # POST invalid mapping
    def test_create_mapping_invalid(self):

        data = {
            "vendor": "",
            "product": ""
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # GET /api/vendor-product-mappings/{id}/
    def test_retrieve_mapping(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["vendor"], self.vendor.id)


    # GET mapping not found
    def test_retrieve_mapping_not_found(self):

        response = self.client.get("/api/vendor-product-mappings/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PUT /api/vendor-product-mappings/{id}/
    def test_full_update_mapping(self):

        new_product = Product.objects.create(
            name="Keyboard",
            code="KEY001"
        )

        data = {
            "vendor": self.vendor.id,
            "product": new_product.id,
            "is_primary": False
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.mapping.refresh_from_db()
        self.assertEqual(self.mapping.product.id, new_product.id)


    # PATCH /api/vendor-product-mappings/{id}/
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
            "vendor": ""
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # DELETE /api/vendor-product-mappings/{id}/
    def test_delete_mapping(self):

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VendorProductMapping.objects.count(), 0)


    # DELETE mapping not found
    def test_delete_mapping_not_found(self):

        response = self.client.delete("/api/vendor-product-mappings/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
