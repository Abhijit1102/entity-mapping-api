from client.course import CourseAPIClient
from models.course import CourseCreate, CourseUpdate


def run_course_tests():

    print("\nRunning Course API tests")

    client = CourseAPIClient()

    # CREATE
    course = client.create_course(
        CourseCreate(
            name="Machine Learning",
            code="ML001",
            description="Intro to ML"
        )
    )
    print("Created:", course)

    # LIST
    courses = client.list_courses()
    print("All Courses:", courses)

    # GET
    course = client.get_course(course.id)
    print("Retrieved:", course)

    # UPDATE
    updated = client.update_course(
        course.id,
        CourseUpdate(
            name="Machine Learning Advanced",
            code="ML001",
            description="Updated ML course"
        )
    )
    print("Updated:", updated)

    # PATCH
    patched = client.partial_update_course(
        course.id,
        CourseUpdate(description="Patched description")
    )
    print("Patched:", patched)

    # DELETE
    client.delete_course(course.id)
    print("Deleted course")
