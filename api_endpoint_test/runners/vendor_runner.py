import logging
import requests

from client.vendor import VendorAPIClient
from models.entities import VendorCreate

logger = logging.getLogger(__name__)


def _assert(condition: bool, message: str):
    if not condition:
        logger.error(f"  FAIL — {message}")
        raise AssertionError(message)
    logger.info(f"  PASS — {message}")


def run_vendor_tests():
    logger.info("Running Vendor API Tests")

    client = VendorAPIClient()

    # ── LIST (baseline) ───────────────────────────────────────
    initial = client.list_vendors()
    _assert(isinstance(initial, list), "List returns a list")

    # ── CREATE ────────────────────────────────────────────────
    vendor = client.create_vendor(
        VendorCreate(name="Microsoft", code="VND-MSF-01", description="Cloud provider")
    )
    _assert(vendor.id is not None,              "Create returns an ID")
    _assert(vendor.name == "Microsoft",         "Create — name matches")
    _assert(vendor.code == "VND-MSF-01",        "Create — code matches")
    _assert(vendor.description == "Cloud provider", "Create — description matches")
    _assert(vendor.is_active is True,           "Create — is_active defaults to True")

    try:

        # ── LIST (contains new record) ────────────────────────
        vendors = client.list_vendors()
        ids = [v.id for v in vendors]
        _assert(vendor.id in ids, "List contains newly created vendor")

        # ── DUPLICATE code blocked ────────────────────────────
        try:
            client.create_vendor(
                VendorCreate(name="Microsoft Duplicate", code="VND-MSF-01")
            )
            _assert(False, "Duplicate code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Duplicate code returns 400")

        # ── GET ───────────────────────────────────────────────
        fetched = client.get_vendor(vendor.id)
        _assert(fetched.id   == vendor.id,   "Retrieve vendor by ID")
        _assert(fetched.name == "Microsoft", "Retrieve — name matches")
        _assert(fetched.code == "VND-MSF-01","Retrieve — code matches")

        # ── GET — not found ───────────────────────────────────
        try:
            client.get_vendor(99999)
            _assert(False, "Get non-existent vendor should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Get non-existent vendor returns 404")

        # ── PUT (full update) ─────────────────────────────────
        updated = client.update_vendor(
            vendor.id,
            VendorCreate(name="Microsoft Corp", code="VND-MSF-01", description="Updated description")
        )
        _assert(updated.name        == "Microsoft Corp",      "PUT — name updated")
        _assert(updated.description == "Updated description", "PUT — description updated")
        _assert(updated.code        == "VND-MSF-01",          "PUT — code unchanged")

        # ── PUT — not found ───────────────────────────────────
        try:
            client.update_vendor(
                99999,
                VendorCreate(name="Ghost", code="VND-GHOST-01")
            )
            _assert(False, "PUT non-existent vendor should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PUT non-existent vendor returns 404")

        # ── PATCH (partial update) ────────────────────────────
        patched = client.partial_update_vendor(vendor.id, {"description": "Patched description"})
        _assert(patched.description == "Patched description", "PATCH — description updated")
        _assert(patched.name        == "Microsoft Corp",      "PATCH — name unchanged")

        # ── PATCH — not found ─────────────────────────────────
        try:
            client.partial_update_vendor(99999, {"description": "x"})
            _assert(False, "PATCH non-existent vendor should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PATCH non-existent vendor returns 404")

        # ── PATCH — invalid field ─────────────────────────────
        try:
            client.partial_update_vendor(vendor.id, {"code": ""})
            _assert(False, "PATCH with empty code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "PATCH with empty code returns 400")

    finally:
        # ── DELETE ────────────────────────────────────────────
        client.delete_vendor(vendor.id)
        vendors_after = client.list_vendors()
        ids_after = [v.id for v in vendors_after]
        _assert(vendor.id not in ids_after, "Delete — vendor no longer in list")

        # ── DELETE — not found ────────────────────────────────
        try:
            client.delete_vendor(vendor.id)
            _assert(False, "Delete non-existent vendor should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Delete non-existent vendor returns 404")

    logger.info("Vendor API Tests complete")
