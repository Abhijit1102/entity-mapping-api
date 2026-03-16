import sys
import os

# Ensure the project root is on sys.path so sibling packages resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import argparse
from runners.vendor_product_mapping_runner import run_vendor_product_mapping_tests
from runners.product_course_mapping_runner import run_product_course_mapping_tests
from runners.course_certification_mapping_runner import run_course_certification_mapping_tests


def main():
    parser = argparse.ArgumentParser(description="Mapping API Test Runner")

    parser.add_argument("--test-all",                       action="store_true", help="Run all mapping tests")
    parser.add_argument("--test-vendor-product-mapping",    action="store_true", help="Run Vendor → Product mapping tests")
    parser.add_argument("--test-product-course-mapping",    action="store_true", help="Run Product → Course mapping tests")
    parser.add_argument("--test-course-certification-mapping", action="store_true", help="Run Course → Certification mapping tests")

    args = parser.parse_args()

    if args.test_all:
        run_vendor_product_mapping_tests()
        run_product_course_mapping_tests()
        run_course_certification_mapping_tests()

    elif args.test_vendor_product_mapping:
        run_vendor_product_mapping_tests()

    elif args.test_product_course_mapping:
        run_product_course_mapping_tests()

    elif args.test_course_certification_mapping:
        run_course_certification_mapping_tests()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
