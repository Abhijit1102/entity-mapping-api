from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product


class ProductAPITestCase(APITestCase):

    def setUp(self):
        """Create initial product"""
        self.product = Product.objects.create(
            name="Cloud Suite",
            code="CS01",
            description="Cloud training product"
        )

        self.list_url = "/api/products/"
        self.detail_url = f"/api/products/{self.product.id}/"

    # GET /api/products/
    def test_list_products(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # POST /api/products/
    def test_create_product(self):
        data = {
            "name": "AI Platform",
            "code": "AI01",
            "description": "Artificial intelligence product"
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    # POST invalid product
    def test_create_product_invalid(self):
        data = {
            "name": ""
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # GET /api/products/{id}/
    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Cloud Suite")

    # GET product not found
    def test_retrieve_product_not_found(self):
        response = self.client.get("/api/products/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PUT /api/products/{id}/
    def test_full_update_product(self):
        data = {
            "name": "Updated Product",
            "code": "CS01",
            "description": "Updated description"
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    # PATCH /api/products/{id}/
    def test_partial_update_product(self):
        data = {
            "description": "Partially updated description"
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.description, "Partially updated description")

    # PATCH invalid field
    def test_partial_update_invalid(self):
        data = {
            "name": ""
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE /api/products/{id}/
    def test_delete_product(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    # DELETE product not found
    def test_delete_product_not_found(self):
        response = self.client.delete("/api/products/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
