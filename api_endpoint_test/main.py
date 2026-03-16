import argparse
from runners.vendor_runner import run_vendor_tests
from runners.product_runner import run_product_tests
from runners.course_runner import run_course_tests
from runners.certification_runner import run_certification_tests


def main():
    parser = argparse.ArgumentParser(description="API Test Runner")

    parser.add_argument("--test-all", action="store_true")
    parser.add_argument("--test-vendor", action="store_true")
    parser.add_argument("--test-product", action="store_true")
    parser.add_argument("--test-course", action="store_true")
    parser.add_argument("--test-certification", action="store_true")

    args = parser.parse_args()

    if args.test_all:
        run_vendor_tests()
        run_product_tests()
        run_course_tests()
        run_certification_tests()

    elif args.test_vendor:
        run_vendor_tests()

    elif args.test_product:
        run_product_tests()

    elif args.test_course:
        run_course_tests()

    elif args.test_certification:
        run_certification_tests()

    else:
        print("Use --help to see available commands")


if __name__ == "__main__":
    main()
