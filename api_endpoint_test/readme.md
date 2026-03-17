# 🧪 Entity Mapping API — Endpoint Test Suite

> A standalone, dependency-light API test runner for the **Entity Mapping API** — built with `requests` and `pydantic`, completely independent of the Django project.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/requests-2.x-orange)
![Pydantic](https://img.shields.io/badge/pydantic-v2-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Tests](#running-the-tests)
- [Test Coverage](#test-coverage)
- [Log Output](#log-output)
- [How It Works](#how-it-works)
- [Adding New Tests](#adding-new-tests)

---

## 📖 Overview

This test suite hits the live **Entity Mapping API** server over HTTP and verifies every endpoint end-to-end. It is completely separate from the Django project — no Django test client, no `pytest`, no database access. It only needs the server to be running.

### What it tests

| Suite | Endpoints Tested |
|---|---|
| Vendor | `/api/vendors/` |
| Product | `/api/products/` |
| Course | `/api/courses/` |
| Certification | `/api/certifications/` |
| Vendor → Product Mapping | `/api/vendor-product-mappings/` |
| Product → Course Mapping | `/api/product-course-mappings/` |
| Course → Certification Mapping | `/api/course-certification-mappings/` |

### Design principles

- **Zero Django dependency** — runs as a plain Python script, completely outside the Django project
- **Self-contained** — seeds its own test data and tears it down after every run, leaving the database empty
- **Logged** — every PASS/FAIL is written to both the console and a timestamped log file under `logs/`
- **Modular** — each entity has its own client, runner, and Pydantic model; adding a new suite takes minutes

---

## 🗂️ Project Structure

```
api_endpoint_test/
│
├── main.py                              # Entry point — argument parsing, logging setup, summary
│
├── models/
│   ├── entities.py                      # Pydantic models: Vendor, Product, Course, Certification
│   └── mappings.py                      # Pydantic models: all 3 mapping types
│
├── client/
│   ├── seed.py                          # Helper: creates/deletes master entities for test setup
│   ├── vendor.py                        # HTTP client for /api/vendors/
│   ├── product.py                       # HTTP client for /api/products/
│   ├── course.py                        # HTTP client for /api/courses/
│   ├── certification.py                 # HTTP client for /api/certifications/
│   ├── vendor_product_mapping.py        # HTTP client for /api/vendor-product-mappings/
│   ├── product_course_mapping.py        # HTTP client for /api/product-course-mappings/
│   └── course_certification_mapping.py  # HTTP client for /api/course-certification-mappings/
│
├── runners/
│   ├── vendor_runner.py                 # Test logic for Vendor API
│   ├── product_runner.py                # Test logic for Product API
│   ├── course_runner.py                 # Test logic for Course API
│   ├── certification_runner.py          # Test logic for Certification API
│   ├── vendor_product_mapping_runner.py
│   ├── product_course_mapping_runner.py
│   └── course_certification_mapping_runner.py
│
└── logs/
    └── test_run_YYYYMMDD_HHMMSS.log     # Auto-generated per run
```

---

## ✅ Prerequisites

- Python **3.10+**
- The **Entity Mapping API server must be running** at `http://127.0.0.1:8000` before executing any tests
- The database should ideally be **empty** before a full run (the suite cleans up after itself but assumes a clean state at the start)

Start the Django server first:

```bash
# from the entity-mapping-api project root
python manage.py runserver
```

---

## ⚙️ Installation

### Step 1 — Navigate to the test folder

```bash
cd api_endpoint_test
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install requests pydantic
```

Or if you are using `uv`:

```bash
uv add requests pydantic
```

---

## 🚀 Running the Tests

### Run all 7 suites

```bash
python main.py --test-all
```

```bash
# using uv
uv run main.py --test-all
```

---

### Run individual suites

#### Master entities

```bash
python main.py --test-vendor
python main.py --test-product
python main.py --test-course
python main.py --test-certification
```

#### Mapping entities

```bash
python main.py --test-vendor-product-mapping
python main.py --test-product-course-mapping
python main.py --test-course-certification-mapping
```

---

### Run multiple specific suites

Flags can be combined freely:

```bash
python main.py --test-vendor --test-product
python main.py --test-vendor-product-mapping --test-product-course-mapping
```

---

### Show help

```bash
python main.py --help
```

```
usage: main.py [-h] [--test-all]
               [--test-vendor] [--test-product]
               [--test-course] [--test-certification]
               [--test-vendor-product-mapping]
               [--test-product-course-mapping]
               [--test-course-certification-mapping]
```

---

## 🔍 Test Coverage

Each suite covers the following scenarios:

### Master entity suites (Vendor / Product / Course / Certification)

| # | Test |
|---|---|
| 1 | List returns a list |
| 2 | Create returns an ID with correct fields |
| 3 | is_active defaults to True on create |
| 4 | List contains the newly created record |
| 5 | Duplicate `code` is blocked (400) |
| 6 | Retrieve by ID returns correct data |
| 7 | Retrieve non-existent ID returns 404 |
| 8 | PUT updates name and description |
| 9 | PUT non-existent ID returns 404 |
| 10 | PATCH updates a single field |
| 11 | PATCH leaves other fields unchanged |
| 12 | PATCH non-existent ID returns 404 |
| 13 | PATCH with empty `code` returns 400 |
| 14 | DELETE removes the record |
| 15 | DELETE non-existent ID returns 404 |

### Mapping suites (VendorProduct / ProductCourse / CourseCertification)

| # | Test |
|---|---|
| 1 | List returns a list on empty DB |
| 2 | Create returns an ID with correct FK fields |
| 3 | is_primary is set correctly on create |
| 4 | List returns 1 mapping after create |
| 5 | Filter by parent ID returns correct results |
| 6 | Filter by child ID returns correct results |
| 7 | Filter by unknown ID returns empty list |
| 8 | Retrieve by ID returns correct data |
| 9 | Retrieve non-existent ID returns 404 |
| 10 | Duplicate mapping (same parent + child) is blocked (400) |
| 11 | Second `is_primary=True` for the same parent is blocked (400) |
| 12 | PUT updates the child FK and is_primary |
| 13 | PUT non-existent ID returns 404 |
| 14 | PATCH toggles is_primary correctly |
| 15 | PATCH non-existent ID returns 404 |
| 16 | DELETE removes the mapping |
| 17 | List is empty after delete |
| 18 | DELETE non-existent ID returns 404 |

---

## 📋 Log Output

Every run automatically creates a timestamped log file at:

```
logs/test_run_YYYYMMDD_HHMMSS.log
```

Logs are written to **both the console and the file simultaneously**.

### Sample log

```
2026-03-16 17:25:06  INFO      =======================================================
2026-03-16 17:25:06  INFO        API TEST RUNNER STARTED
2026-03-16 17:25:06  INFO        Log file: logs/test_run_20260316_172506.log
2026-03-16 17:25:06  INFO      =======================================================

2026-03-16 17:25:06  INFO      =======================================================
2026-03-16 17:25:06  INFO      START  Vendor
2026-03-16 17:25:06  INFO      =======================================================
2026-03-16 17:25:06  INFO      Running Vendor API Tests
2026-03-16 17:25:07  INFO        PASS — List returns a list
2026-03-16 17:25:07  INFO        PASS — Create returns an ID
...
2026-03-16 17:25:08  INFO      RESULT ✓  Vendor — ALL TESTS PASSED

...

2026-03-16 17:25:12  INFO      =======================================================
2026-03-16 17:25:12  INFO        TEST RUN SUMMARY
2026-03-16 17:25:12  INFO        Suites passed : 7
2026-03-16 17:25:12  INFO        Suites failed : 0
2026-03-16 17:25:12  INFO        Total suites  : 7
2026-03-16 17:25:12  INFO      =======================================================
```

---

## ⚙️ How It Works

### Seed and teardown

The mapping runners need master entities (Vendor, Product, Course, Certification) to exist before they can create mappings. The `client/seed.py` helper creates them at the start of each mapping runner and deletes them in a `finally` block — so the database is always cleaned up even if a test fails mid-run.

```
Mapping runner starts
    → seed.py creates Vendor + Product (or Course + Certification)
    → tests run against the mapping endpoints
    → finally: seed.py deletes the seeded entities
Mapping runner ends — DB is empty again
```

### Unique codes

Every seeded entity uses a runner-specific code prefix (e.g. `VND-VPM-01`, `PROD-PCM-01`) to prevent collisions when multiple suites run in the same session.

### Assertion helper

Each runner uses a shared `_assert(condition, message)` function that logs `PASS` or `FAIL` and raises `AssertionError` on failure, which is caught by the `run()` wrapper in `main.py`.

---

## ➕ Adding New Tests

To add a test suite for a new entity:

1. **Add Pydantic models** to `models/entities.py` or `models/mappings.py`
2. **Create a client** in `client/your_entity.py` with list / get / create / update / patch / delete methods
3. **Create a runner** in `runners/your_entity_runner.py` following the existing pattern
4. **Register in `main.py`** — add the import, a new `--test-your-entity` flag, and a `run(...)` call

---

## 📄 License

This project is licensed under the **MIT License**.
