from rest_framework.test import APITestCase
from rest_framework import status

from product.models import Product
from course.models import Course
from .models import ProductCourseMapping


class ProductCourseMappingAPITestCase(APITestCase):

    def setUp(self):
        """Create initial data"""

        self.product = Product.objects.create(
            name="Cloud Suite Pro",
            code="CSP001",
            description="Enterprise cloud management product"
        )

        self.course = Course.objects.create(
            name="Cloud Fundamentals",
            code="CF001",
            description="Intro to cloud computing"
        )

        self.mapping = ProductCourseMapping.objects.create(
            product=self.product,
            course=self.course,
            is_primary=True
        )

        self.list_url = "/api/product-course-mappings/"
        self.detail_url = f"/api/product-course-mappings/{self.mapping.id}/"


    # GET /api/product-course-mappings/
    def test_list_mappings(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with product filter
    def test_filter_by_product(self):
        response = self.client.get(f"{self.list_url}?product_id={self.product.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with course filter
    def test_filter_by_course(self):
        response = self.client.get(f"{self.list_url}?course_id={self.course.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # GET with non-matching filter returns empty
    def test_filter_returns_empty_for_unknown_id(self):
        response = self.client.get(f"{self.list_url}?product_id=999")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    # POST /api/product-course-mappings/
    def test_create_mapping(self):

        new_course = Course.objects.create(
            name="Advanced Cloud",
            code="AC001"
        )

        data = {
            "product": self.product.id,
            "course": new_course.id,
            "is_primary": False
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductCourseMapping.objects.count(), 2)


    # POST duplicate mapping
    def test_create_duplicate_mapping(self):

        data = {
            "product": self.product.id,
            "course": self.course.id,
            "is_primary": False
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # POST second primary mapping for same product
    def test_create_second_primary_mapping(self):

        new_course = Course.objects.create(
            name="DevOps Basics",
            code="DOB001"
        )

        data = {
            "product": self.product.id,
            "course": new_course.id,
            "is_primary": True
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # POST invalid mapping (missing fields)
    def test_create_mapping_invalid(self):

        data = {
            "product": "",
            "course": ""
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # GET /api/product-course-mappings/{id}/
    def test_retrieve_mapping(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"], self.product.id)
        self.assertEqual(response.data["course"], self.course.id)


    # GET mapping not found
    def test_retrieve_mapping_not_found(self):

        response = self.client.get("/api/product-course-mappings/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PUT /api/product-course-mappings/{id}/
    def test_full_update_mapping(self):

        new_course = Course.objects.create(
            name="Networking Essentials",
            code="NE001"
        )

        data = {
            "product": self.product.id,
            "course": new_course.id,
            "is_primary": False
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.mapping.refresh_from_db()
        self.assertEqual(self.mapping.course.id, new_course.id)


    # PUT mapping not found
    def test_full_update_mapping_not_found(self):

        data = {
            "product": self.product.id,
            "course": self.course.id,
            "is_primary": False
        }

        response = self.client.put("/api/product-course-mappings/999/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PATCH /api/product-course-mappings/{id}/
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
            "product": ""
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # PATCH mapping not found
    def test_partial_update_not_found(self):

        response = self.client.patch(
            "/api/product-course-mappings/999/",
            {"is_primary": False},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # DELETE /api/product-course-mappings/{id}/
    def test_delete_mapping(self):

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProductCourseMapping.objects.count(), 0)


    # DELETE mapping not found
    def test_delete_mapping_not_found(self):

        response = self.client.delete("/api/product-course-mappings/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
