import logging
import requests

from client.course_certification_mapping import CourseCertificationMappingAPIClient
from client.seed import (
    create_course, create_certification,
    delete_course, delete_certification,
)
from models.mappings import (
    CourseCertificationMappingCreate,
    CourseCertificationMappingUpdate,
)

logger = logging.getLogger(__name__)


def _assert(condition: bool, message: str):
    if not condition:
        logger.error(f"  FAIL — {message}")
        raise AssertionError(message)
    logger.info(f"  PASS — {message}")


def run_course_certification_mapping_tests():
    logger.info("Running Course → Certification Mapping API Tests")

    client = CourseCertificationMappingAPIClient()

    # ── Seed master entities ──────────────────────────────────
    course         = create_course("Cloud Fundamentals",           "CRS-CCM-01")
    certification1 = create_certification("AWS Cloud Practitioner", "CERT-CCM-01")
    certification2 = create_certification("Azure Fundamentals",     "CERT-CCM-02")
    logger.info(f"  Seeded course={course.id}, cert1={certification1.id}, cert2={certification2.id}")

    try:

        # ── LIST (empty) ──────────────────────────────────────
        mappings = client.list_mappings()
        _assert(isinstance(mappings, list), "List returns a list on empty DB")

        # ── CREATE ────────────────────────────────────────────
        mapping = client.create_mapping(
            CourseCertificationMappingCreate(
                course=course.id,
                certification=certification1.id,
                is_primary=True
            )
        )
        _assert(mapping.id is not None,                     "Create returns an ID")
        _assert(mapping.course        == course.id,         "Create — course ID matches")
        _assert(mapping.certification == certification1.id, "Create — certification ID matches")
        _assert(mapping.is_primary is True,                 "Create — is_primary is True")

        # ── LIST (1 item) ─────────────────────────────────────
        mappings = client.list_mappings()
        _assert(len(mappings) == 1, "List returns 1 mapping after create")

        # ── FILTER by course_id ───────────────────────────────
        filtered = client.list_mappings(course_id=course.id)
        _assert(len(filtered) == 1, "Filter by course_id returns 1 result")

        # ── FILTER by certification_id ────────────────────────
        filtered = client.list_mappings(certification_id=certification1.id)
        _assert(len(filtered) == 1, "Filter by certification_id returns 1 result")

        # ── FILTER — unknown ID returns empty ─────────────────
        filtered = client.list_mappings(course_id=99999)
        _assert(len(filtered) == 0, "Filter by unknown course_id returns empty list")

        # ── GET ───────────────────────────────────────────────
        fetched = client.get_mapping(mapping.id)
        _assert(fetched.id == mapping.id, "Retrieve mapping by ID")

        # ── GET — not found ───────────────────────────────────
        try:
            client.get_mapping(99999)
            _assert(False, "Get non-existent mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Get non-existent mapping returns 404")

        # ── DUPLICATE mapping blocked ─────────────────────────
        try:
            client.create_mapping(
                CourseCertificationMappingCreate(
                    course=course.id,
                    certification=certification1.id,
                    is_primary=False
                )
            )
            _assert(False, "Duplicate mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Duplicate mapping returns 400")

        # ── SECOND is_primary blocked ─────────────────────────
        try:
            client.create_mapping(
                CourseCertificationMappingCreate(
                    course=course.id,
                    certification=certification2.id,
                    is_primary=True
                )
            )
            _assert(False, "Second primary mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Second primary mapping returns 400")

        # ── PUT (full update) ─────────────────────────────────
        updated = client.update_mapping(
            mapping.id,
            CourseCertificationMappingUpdate(
                course=course.id,
                certification=certification2.id,
                is_primary=False
            )
        )
        _assert(updated.certification == certification2.id, "PUT — certification updated")
        _assert(updated.is_primary is False,                "PUT — is_primary updated to False")

        # ── PUT — not found ───────────────────────────────────
        try:
            client.update_mapping(
                99999,
                CourseCertificationMappingUpdate(
                    course=course.id,
                    certification=certification2.id,
                    is_primary=False
                )
            )
            _assert(False, "PUT non-existent mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PUT non-existent mapping returns 404")

        # ── PATCH (partial update) ────────────────────────────
        patched = client.partial_update_mapping(
            mapping.id,
            CourseCertificationMappingUpdate(is_primary=True)
        )
        _assert(patched.is_primary is True, "PATCH — is_primary toggled back to True")

        # ── PATCH — not found ─────────────────────────────────
        try:
            client.partial_update_mapping(
                99999,
                CourseCertificationMappingUpdate(is_primary=False)
            )
            _assert(False, "PATCH non-existent mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PATCH non-existent mapping returns 404")

        # ── DELETE ────────────────────────────────────────────
        client.delete_mapping(mapping.id)
        mappings_after = client.list_mappings()
        _assert(len(mappings_after) == 0, "Delete — list is empty after delete")

        # ── DELETE — not found ────────────────────────────────
        try:
            client.delete_mapping(99999)
            _assert(False, "Delete non-existent mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Delete non-existent mapping returns 404")

    finally:
        delete_certification(certification1.id)
        delete_certification(certification2.id)
        delete_course(course.id)
        logger.info(f"  Teardown complete — course={course.id}, cert1={certification1.id}, cert2={certification2.id}")
