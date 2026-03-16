import logging
import requests

from client.course import CourseAPIClient
from models.entities import CourseCreate

logger = logging.getLogger(__name__)


def _assert(condition: bool, message: str):
    if not condition:
        logger.error(f"  FAIL — {message}")
        raise AssertionError(message)
    logger.info(f"  PASS — {message}")


def run_course_tests():
    logger.info("Running Course API Tests")

    client = CourseAPIClient()

    # ── LIST (baseline) ───────────────────────────────────────
    initial = client.list_courses()
    _assert(isinstance(initial, list), "List returns a list")

    # ── CREATE ────────────────────────────────────────────────
    course = client.create_course(
        CourseCreate(name="Cloud Fundamentals", code="CRS-CLF-01", description="Intro to cloud")
    )
    _assert(course.id is not None,                  "Create returns an ID")
    _assert(course.name == "Cloud Fundamentals",    "Create — name matches")
    _assert(course.code == "CRS-CLF-01",            "Create — code matches")
    _assert(course.description == "Intro to cloud", "Create — description matches")
    _assert(course.is_active is True,               "Create — is_active defaults to True")

    try:

        # ── LIST (contains new record) ────────────────────────
        courses = client.list_courses()
        ids = [c.id for c in courses]
        _assert(course.id in ids, "List contains newly created course")

        # ── DUPLICATE code blocked ────────────────────────────
        try:
            client.create_course(
                CourseCreate(name="Cloud Fundamentals Duplicate", code="CRS-CLF-01")
            )
            _assert(False, "Duplicate code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Duplicate code returns 400")

        # ── GET ───────────────────────────────────────────────
        fetched = client.get_course(course.id)
        _assert(fetched.id   == course.id,          "Retrieve course by ID")
        _assert(fetched.name == "Cloud Fundamentals","Retrieve — name matches")
        _assert(fetched.code == "CRS-CLF-01",        "Retrieve — code matches")

        # ── GET — not found ───────────────────────────────────
        try:
            client.get_course(99999)
            _assert(False, "Get non-existent course should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Get non-existent course returns 404")

        # ── PUT (full update) ─────────────────────────────────
        updated = client.update_course(
            course.id,
            CourseCreate(name="Cloud Fundamentals v2", code="CRS-CLF-01", description="Updated description")
        )
        _assert(updated.name        == "Cloud Fundamentals v2", "PUT — name updated")
        _assert(updated.description == "Updated description",   "PUT — description updated")
        _assert(updated.code        == "CRS-CLF-01",            "PUT — code unchanged")

        # ── PUT — not found ───────────────────────────────────
        try:
            client.update_course(
                99999,
                CourseCreate(name="Ghost", code="CRS-GHOST-01")
            )
            _assert(False, "PUT non-existent course should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PUT non-existent course returns 404")

        # ── PATCH (partial update) ────────────────────────────
        patched = client.partial_update_course(course.id, {"description": "Patched description"})
        _assert(patched.description == "Patched description",   "PATCH — description updated")
        _assert(patched.name        == "Cloud Fundamentals v2", "PATCH — name unchanged")

        # ── PATCH — not found ─────────────────────────────────
        try:
            client.partial_update_course(99999, {"description": "x"})
            _assert(False, "PATCH non-existent course should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PATCH non-existent course returns 404")

        # ── PATCH — invalid field ─────────────────────────────
        try:
            client.partial_update_course(course.id, {"code": ""})
            _assert(False, "PATCH with empty code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "PATCH with empty code returns 400")

    finally:
        # ── DELETE ────────────────────────────────────────────
        client.delete_course(course.id)
        courses_after = client.list_courses()
        ids_after = [c.id for c in courses_after]
        _assert(course.id not in ids_after, "Delete — course no longer in list")

        # ── DELETE — not found ────────────────────────────────
        try:
            client.delete_course(course.id)
            _assert(False, "Delete non-existent course should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Delete non-existent course returns 404")

    logger.info("Course API Tests complete")
