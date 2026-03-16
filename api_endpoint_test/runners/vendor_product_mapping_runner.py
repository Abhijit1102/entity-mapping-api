import logging
import requests

from client.vendor_product_mapping import VendorProductMappingAPIClient
from client.seed import (
    create_vendor, create_product,
    delete_vendor, delete_product,
)
from models.mappings import VendorProductMappingCreate, VendorProductMappingUpdate

logger = logging.getLogger(__name__)

MAPPING_URL = "http://127.0.0.1:8000/api/vendor-product-mappings/"


def _assert(condition: bool, message: str):
    if not condition:
        logger.error(f"  FAIL — {message}")
        raise AssertionError(message)
    logger.info(f"  PASS — {message}")


def run_vendor_product_mapping_tests():
    logger.info("Running Vendor → Product Mapping API Tests")

    client = VendorProductMappingAPIClient()

    # ── Seed master entities ──────────────────────────────────
    vendor   = create_vendor("Acme Corp", "ACME-VPM-01")
    product1 = create_product("Cloud Suite", "PROD-VPM-01")
    product2 = create_product("Data Hub",    "PROD-VPM-02")
    logger.info(f"  Seeded vendor={vendor.id}, product1={product1.id}, product2={product2.id}")

    try:

        # ── LIST (empty) ──────────────────────────────────────
        mappings = client.list_mappings()
        _assert(isinstance(mappings, list), "List returns a list on empty DB")

        # ── CREATE ────────────────────────────────────────────
        mapping = client.create_mapping(
            VendorProductMappingCreate(
                vendor=vendor.id,
                product=product1.id,
                is_primary=True
            )
        )
        _assert(mapping.id is not None,         "Create returns an ID")
        _assert(mapping.vendor  == vendor.id,   "Create — vendor ID matches")
        _assert(mapping.product == product1.id, "Create — product ID matches")
        _assert(mapping.is_primary is True,     "Create — is_primary is True")

        # ── LIST (1 item) ─────────────────────────────────────
        mappings = client.list_mappings()
        _assert(len(mappings) == 1, "List returns 1 mapping after create")

        # ── FILTER by vendor_id ───────────────────────────────
        filtered = client.list_mappings(vendor_id=vendor.id)
        _assert(len(filtered) == 1, "Filter by vendor_id returns 1 result")

        # ── FILTER by product_id ──────────────────────────────
        filtered = client.list_mappings(product_id=product1.id)
        _assert(len(filtered) == 1, "Filter by product_id returns 1 result")

        # ── FILTER — unknown ID returns empty ─────────────────
        filtered = client.list_mappings(vendor_id=99999)
        _assert(len(filtered) == 0, "Filter by unknown vendor_id returns empty list")

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
                VendorProductMappingCreate(
                    vendor=vendor.id,
                    product=product1.id,
                    is_primary=False
                )
            )
            _assert(False, "Duplicate mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Duplicate mapping returns 400")

        # ── SECOND is_primary blocked ─────────────────────────
        try:
            client.create_mapping(
                VendorProductMappingCreate(
                    vendor=vendor.id,
                    product=product2.id,
                    is_primary=True
                )
            )
            _assert(False, "Second primary mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Second primary mapping returns 400")

        # ── PUT (full update) ─────────────────────────────────
        updated = client.update_mapping(
            mapping.id,
            VendorProductMappingUpdate(
                vendor=vendor.id,
                product=product2.id,
                is_primary=False
            )
        )
        _assert(updated.product == product2.id, "PUT — product updated")
        _assert(updated.is_primary is False,    "PUT — is_primary updated to False")

        # ── PUT — not found ───────────────────────────────────
        try:
            client.update_mapping(
                99999,
                VendorProductMappingUpdate(
                    vendor=vendor.id,
                    product=product2.id,
                    is_primary=False
                )
            )
            _assert(False, "PUT non-existent mapping should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PUT non-existent mapping returns 404")

        # ── PATCH (partial update) ────────────────────────────
        patched = client.partial_update_mapping(
            mapping.id,
            VendorProductMappingUpdate(is_primary=True)
        )
        _assert(patched.is_primary is True, "PATCH — is_primary toggled back to True")

        # ── PATCH — not found ─────────────────────────────────
        try:
            client.partial_update_mapping(
                99999,
                VendorProductMappingUpdate(is_primary=False)
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
        delete_product(product1.id)
        delete_product(product2.id)
        delete_vendor(vendor.id)
        logger.info(f"  Teardown complete — vendor={vendor.id}, product1={product1.id}, product2={product2.id}")
