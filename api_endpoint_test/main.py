import sys
import os
import logging
from datetime import datetime

# Ensure the project root is on sys.path so sibling packages resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import argparse

# ── Master entity runners ─────────────────────────────────────────────────────
from runners.vendor_runner import run_vendor_tests
from runners.product_runner import run_product_tests
from runners.course_runner import run_course_tests
from runners.certification_runner import run_certification_tests

# ── Mapping runners ───────────────────────────────────────────────────────────
from runners.vendor_product_mapping_runner import run_vendor_product_mapping_tests
from runners.product_course_mapping_runner import run_product_course_mapping_tests
from runners.course_certification_mapping_runner import run_course_certification_mapping_tests


# ── Logging setup ─────────────────────────────────────────────────────────────

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(
    LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────

PASS_COUNT = 0
FAIL_COUNT = 0


def run(name: str, fn):
    """Wrap a runner, catch exceptions, and log pass/fail outcome."""
    global PASS_COUNT, FAIL_COUNT

    logger.info("=" * 55)
    logger.info(f"START  {name}")
    logger.info("=" * 55)
    try:
        fn()
        logger.info(f"RESULT ✓  {name} — ALL TESTS PASSED")
        PASS_COUNT += 1
    except AssertionError as e:
        logger.error(f"RESULT ✗  {name} — ASSERTION FAILED: {e}")
        FAIL_COUNT += 1
    except Exception as e:
        logger.exception(f"RESULT ✗  {name} — UNEXPECTED ERROR: {e}")
        FAIL_COUNT += 1
    finally:
        logger.info("")


def main():
    parser = argparse.ArgumentParser(description="Full API Test Runner")

    # run everything
    parser.add_argument("--test-all",                          action="store_true", help="Run every test suite")

    # master entities
    parser.add_argument("--test-vendor",                       action="store_true", help="Run Vendor tests")
    parser.add_argument("--test-product",                      action="store_true", help="Run Product tests")
    parser.add_argument("--test-course",                       action="store_true", help="Run Course tests")
    parser.add_argument("--test-certification",                action="store_true", help="Run Certification tests")

    # mappings
    parser.add_argument("--test-vendor-product-mapping",       action="store_true", help="Run Vendor → Product mapping tests")
    parser.add_argument("--test-product-course-mapping",       action="store_true", help="Run Product → Course mapping tests")
    parser.add_argument("--test-course-certification-mapping", action="store_true", help="Run Course → Certification mapping tests")

    args = parser.parse_args()

    logger.info("=" * 55)
    logger.info("  API TEST RUNNER STARTED")
    logger.info(f"  Log file: {log_filename}")
    logger.info("=" * 55)
    logger.info("")

    if args.test_all:
        run("Vendor",                         run_vendor_tests)
        run("Product",                        run_product_tests)
        run("Course",                         run_course_tests)
        run("Certification",                  run_certification_tests)
        run("Vendor → Product Mapping",       run_vendor_product_mapping_tests)
        run("Product → Course Mapping",       run_product_course_mapping_tests)
        run("Course → Certification Mapping", run_course_certification_mapping_tests)

    else:
        if args.test_vendor:
            run("Vendor", run_vendor_tests)
        if args.test_product:
            run("Product", run_product_tests)
        if args.test_course:
            run("Course", run_course_tests)
        if args.test_certification:
            run("Certification", run_certification_tests)
        if args.test_vendor_product_mapping:
            run("Vendor → Product Mapping", run_vendor_product_mapping_tests)
        if args.test_product_course_mapping:
            run("Product → Course Mapping", run_product_course_mapping_tests)
        if args.test_course_certification_mapping:
            run("Course → Certification Mapping", run_course_certification_mapping_tests)

        if not any(vars(args).values()):
            parser.print_help()
            return

    # ── Summary ───────────────────────────────────────────────
    logger.info("=" * 55)
    logger.info("  TEST RUN SUMMARY")
    logger.info(f"  Suites passed : {PASS_COUNT}")
    logger.info(f"  Suites failed : {FAIL_COUNT}")
    logger.info(f"  Total suites  : {PASS_COUNT + FAIL_COUNT}")
    logger.info("=" * 55)


if __name__ == "__main__":
    main()
