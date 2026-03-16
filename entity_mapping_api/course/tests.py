from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course


class CourseAPITestCase(APITestCase):

    def setUp(self):
        """Create initial course"""

        self.course = Course.objects.create(
            name="Python for Beginners",
            code="PY001",
            description="Learn Python",
            is_active=True
        )

        self.list_url = reverse("course-list")
        self.detail_url = reverse("course-detail", args=[self.course.id])


    # GET list
    def test_list_courses(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # POST create
    def test_create_course(self):

        data = {
            "name": "Django REST Framework",
            "code": "DRF001",
            "description": "API Development",
            "is_active": True
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)


    # POST invalid
    def test_create_course_invalid(self):

        data = {
            "name": "",
            "code": "",
            "description": "Invalid Course"
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # GET detail
    def test_retrieve_course(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Python for Beginners")


    # GET not found
    def test_retrieve_course_not_found(self):

        url = reverse("course-detail", args=[999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # PUT update
    def test_full_update_course(self):

        data = {
            "name": "Python Advanced",
            "code": "PY001",
            "description": "Advanced Python",
            "is_active": True
        }

        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Python Advanced")


    # PATCH update
    def test_partial_update_course(self):

        data = {
            "description": "Updated description"
        }

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.course.refresh_from_db()
        self.assertEqual(self.course.description, "Updated description")


    # PATCH invalid
    def test_partial_update_invalid(self):

        data = {"name": ""}

        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # DELETE
    def test_delete_course(self):

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


    # DELETE not found
    def test_delete_course_not_found(self):

        url = reverse("course-detail", args=[999])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
