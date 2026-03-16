import logging
import requests

from client.product import ProductAPIClient
from models.entities import ProductCreate

logger = logging.getLogger(__name__)


def _assert(condition: bool, message: str):
    if not condition:
        logger.error(f"  FAIL — {message}")
        raise AssertionError(message)
    logger.info(f"  PASS — {message}")


def run_product_tests():
    logger.info("Running Product API Tests")

    client = ProductAPIClient()

    # ── LIST (baseline) ───────────────────────────────────────
    initial = client.list_products()
    _assert(isinstance(initial, list), "List returns a list")

    # ── CREATE ────────────────────────────────────────────────
    product = client.create_product(
        ProductCreate(name="Cloud Suite", code="PRD-CLS-01", description="Enterprise cloud product")
    )
    _assert(product.id is not None,                       "Create returns an ID")
    _assert(product.name == "Cloud Suite",                "Create — name matches")
    _assert(product.code == "PRD-CLS-01",                 "Create — code matches")
    _assert(product.description == "Enterprise cloud product", "Create — description matches")
    _assert(product.is_active is True,                    "Create — is_active defaults to True")

    try:

        # ── LIST (contains new record) ────────────────────────
        products = client.list_products()
        ids = [p.id for p in products]
        _assert(product.id in ids, "List contains newly created product")

        # ── DUPLICATE code blocked ────────────────────────────
        try:
            client.create_product(
                ProductCreate(name="Cloud Suite Duplicate", code="PRD-CLS-01")
            )
            _assert(False, "Duplicate code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "Duplicate code returns 400")

        # ── GET ───────────────────────────────────────────────
        fetched = client.get_product(product.id)
        _assert(fetched.id   == product.id,    "Retrieve product by ID")
        _assert(fetched.name == "Cloud Suite", "Retrieve — name matches")
        _assert(fetched.code == "PRD-CLS-01",  "Retrieve — code matches")

        # ── GET — not found ───────────────────────────────────
        try:
            client.get_product(99999)
            _assert(False, "Get non-existent product should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Get non-existent product returns 404")

        # ── PUT (full update) ─────────────────────────────────
        updated = client.update_product(
            product.id,
            ProductCreate(name="Cloud Suite Pro", code="PRD-CLS-01", description="Updated description")
        )
        _assert(updated.name        == "Cloud Suite Pro",    "PUT — name updated")
        _assert(updated.description == "Updated description","PUT — description updated")
        _assert(updated.code        == "PRD-CLS-01",         "PUT — code unchanged")

        # ── PUT — not found ───────────────────────────────────
        try:
            client.update_product(
                99999,
                ProductCreate(name="Ghost", code="PRD-GHOST-01")
            )
            _assert(False, "PUT non-existent product should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PUT non-existent product returns 404")

        # ── PATCH (partial update) ────────────────────────────
        patched = client.partial_update_product(product.id, {"description": "Patched description"})
        _assert(patched.description == "Patched description", "PATCH — description updated")
        _assert(patched.name        == "Cloud Suite Pro",     "PATCH — name unchanged")

        # ── PATCH — not found ─────────────────────────────────
        try:
            client.partial_update_product(99999, {"description": "x"})
            _assert(False, "PATCH non-existent product should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "PATCH non-existent product returns 404")

        # ── PATCH — invalid field ─────────────────────────────
        try:
            client.partial_update_product(product.id, {"code": ""})
            _assert(False, "PATCH with empty code should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 400, "PATCH with empty code returns 400")

    finally:
        # ── DELETE ────────────────────────────────────────────
        client.delete_product(product.id)
        products_after = client.list_products()
        ids_after = [p.id for p in products_after]
        _assert(product.id not in ids_after, "Delete — product no longer in list")

        # ── DELETE — not found ────────────────────────────────
        try:
            client.delete_product(product.id)
            _assert(False, "Delete non-existent product should raise")
        except requests.HTTPError as e:
            _assert(e.response.status_code == 404, "Delete non-existent product returns 404")

    logger.info("Product API Tests complete")
