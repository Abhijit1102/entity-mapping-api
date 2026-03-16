import requests
from typing import List
from models.course import CourseCreate, CourseUpdate, CourseResponse

BASE_URL = "http://127.0.0.1:8000/api/courses/"


class CourseAPIClient:

    def list_courses(self) -> List[CourseResponse]:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        courses = response.json()
        return [CourseResponse(**c) for c in courses]


    def get_course(self, course_id: int) -> CourseResponse:
        response = requests.get(f"{BASE_URL}{course_id}/")
        response.raise_for_status()

        return CourseResponse(**response.json())


    def create_course(self, course: CourseCreate) -> CourseResponse:
        response = requests.post(BASE_URL, json=course.model_dump())
        response.raise_for_status()

        return CourseResponse(**response.json())


    def update_course(self, course_id: int, course: CourseUpdate) -> CourseResponse:
        response = requests.put(
            f"{BASE_URL}{course_id}/",
            json=course.model_dump()
        )
        response.raise_for_status()

        return CourseResponse(**response.json())


    def partial_update_course(self, course_id: int, course: CourseUpdate) -> CourseResponse:
        response = requests.patch(
            f"{BASE_URL}{course_id}/",
            json=course.model_dump(exclude_none=True)
        )
        response.raise_for_status()

        return CourseResponse(**response.json())


    def delete_course(self, course_id: int) -> None:
        response = requests.delete(f"{BASE_URL}{course_id}/")
        response.raise_for_status()
