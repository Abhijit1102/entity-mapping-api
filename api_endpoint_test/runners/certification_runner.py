import logging
import requests

from client.certification import CertificationAPIClient
from models.entities import CertificationCreate

logger = logging.getLogger(__name__)


def _assert(condition: bool, message: str):
    if not condition:
        logger.error(f"  FAIL — {message}")
        raise AssertionError(message)
    logger.info(f"  PASS — {message}")


def run_certification_tests():
    logger.info("Running Certification API Tests")

    client = CertificationAPIClient()

    # ── LIST (baseline) ───────────────────────────────────────
    initial = client.list_certifications()
    _assert(isinstance(initial, list), "List returns a list")

    # ── CREATE ────────────────────────────────────────────────
    cert = client.create_certification(
        CertificationCreate(name="AWS Cloud Practitioner", code="CRT-AWS-01", description="Entry-level AWS cert")
    )
    _assert(cert.id is not None,                         "Create returns an ID")
    _assert(cert.name == "AWS Cloud Practitioner",       "Create — name matches")
    _assert(cert.code == "CRT-AWS-01",                   "Create — code matches")
    _assert(cert.description == "Entry-level AWS cert",  "Create — description matches")
    _assert(cert.is_active is True,                      "Create — is_active defaults to True")

    try:

        # ── LIST (contains new record) ────────────────────────
        certs = client.list_certifications()
        ids = [c.id for c in certs]
        _assert(cert.id in ids, "List contains newly created certification")

        # ── DUPLICATE code blocked ────────────────────────────
        try:
            client.create_certification(
                CertificationCreate(name="AWS Duplicate", code="CRT-AWS-01")
            )
            _assert(False, "Duplicate code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Duplicate code returns 400")

        # ── GET ───────────────────────────────────────────────
        fetched = client.get_certification(cert.id)
        _assert(fetched.id   == cert.id,                  "Retrieve certification by ID")
        _assert(fetched.name == "AWS Cloud Practitioner", "Retrieve — name matches")
        _assert(fetched.code == "CRT-AWS-01",             "Retrieve — code matches")

        # ── GET — not found ───────────────────────────────────
        try:
            client.get_certification(99999)
            _assert(False, "Get non-existent certification should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Get non-existent certification returns 404")

        # ── PUT (full update) ─────────────────────────────────
        updated = client.update_certification(
            cert.id,
            CertificationCreate(name="AWS CCP v2", code="CRT-AWS-01", description="Updated description")
        )
        _assert(updated.name        == "AWS CCP v2",          "PUT — name updated")
        _assert(updated.description == "Updated description",  "PUT — description updated")
        _assert(updated.code        == "CRT-AWS-01",           "PUT — code unchanged")

        # ── PUT — not found ───────────────────────────────────
        try:
            client.update_certification(
                99999,
                CertificationCreate(name="Ghost", code="CRT-GHOST-01")
            )
            _assert(False, "PUT non-existent certification should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PUT non-existent certification returns 404")

        # ── PATCH (partial update) ────────────────────────────
        patched = client.partial_update_certification(cert.id, {"description": "Patched description"})
        _assert(patched.description == "Patched description", "PATCH — description updated")
        _assert(patched.name        == "AWS CCP v2",          "PATCH — name unchanged")

        # ── PATCH — not found ─────────────────────────────────
        try:
            client.partial_update_certification(99999, {"description": "x"})
            _assert(False, "PATCH non-existent certification should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PATCH non-existent certification returns 404")

        # ── PATCH — invalid field ─────────────────────────────
        try:
            client.partial_update_certification(cert.id, {"code": ""})
            _assert(False, "PATCH with empty code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "PATCH with empty code returns 400")

    finally:
        # ── DELETE ────────────────────────────────────────────
        client.delete_certification(cert.id)
        certs_after = client.list_certifications()
        ids_after = [c.id for c in certs_after]
        _assert(cert.id not in ids_after, "Delete — certification no longer in list")

        # ── DELETE — not found ────────────────────────────────
        try:
            client.delete_certification(cert.id)
            _assert(False, "Delete non-existent certification should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Delete non-existent certification returns 404")

    logger.info("Certification API Tests complete")
