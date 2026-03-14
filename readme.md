# 🗂️ Entity Mapping API

> A modular Django REST Framework backend for managing master entities and their relational mappings — built with clean architecture and core DRF fundamentals.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.x-red)
![Swagger](https://img.shields.io/badge/Docs-Swagger%20%2F%20ReDoc-brightgreen?logo=swagger)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Features](#features)
- [Validation Rules](#validation-rules)
- [API Endpoints](#api-endpoints)
- [Filtering](#filtering)
- [Swagger Documentation](#swagger-documentation)
- [Installation Guide](#installation-guide)
- [Running the Project](#running-the-project)
- [Example API Requests](#example-api-requests)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## 📖 Overview

**Entity Mapping API** is a backend service built with **Django** and **Django REST Framework** that manages a set of master entities and their interconnected mappings. The project is designed with a **modular Django app structure**, where each entity and mapping lives in its own dedicated app.

### Master Entities

| Entity        | Description                                 |
|---------------|---------------------------------------------|
| Vendor        | Represents a supplier or service provider   |
| Product       | Represents a product offered by a vendor    |
| Course        | Represents a course linked to a product     |
| Certification | Represents a certification linked to a course |

### Mapping Entities

| Mapping                  | Relationship              |
|--------------------------|---------------------------|
| VendorProductMapping     | Vendor → Product          |
| ProductCourseMapping     | Product → Course          |
| CourseCertificationMapping | Course → Certification  |

This project is suitable as a **technical assignment submission** or as the foundation for a **production-grade modular backend system**.

---

## 🛠️ Tech Stack

| Technology              | Purpose                                 |
|-------------------------|-----------------------------------------|
| **Python 3.10+**        | Core programming language               |
| **Django 4.x**          | Web framework                           |
| **Django REST Framework** | RESTful API layer                     |
| **drf-yasg**            | Swagger / ReDoc API documentation       |
| **SQLite** *(default)*  | Development database (configurable)     |

### Design Constraints

This project deliberately uses **only** `APIView` for all endpoints. The following DRF abstractions are intentionally excluded to demonstrate a solid understanding of core DRF fundamentals:

- ❌ No `ViewSets`
- ❌ No `GenericAPIView`
- ❌ No `Routers`
- ❌ No `Mixins`

Every view is written explicitly using `APIView`, with manual handling of request parsing, serialization, validation, and responses.

---

## 🏗️ Project Architecture

The project follows a **modular app architecture** — each entity is isolated in its own Django app with its own models, serializers, views, URLs, and admin registration.

```
entity-mapping-api/
│
├── entity-mapping-api/                          # Project settings and root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── vendor/                        # Master: Vendor
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── product/                       # Master: Product
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── course/                        # Master: Course
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── certification/                 # Master: Certification
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── vendor_product_mapping/        # Mapping: Vendor → Product
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── product_course_mapping/        # Mapping: Product → Course
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── course_certification_mapping/  # Mapping: Course → Certification
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── requirements.txt
└── manage.py
```

### App Breakdown

**Master Apps** — manage independent entities with full CRUD:

- `vendor` — Vendor records
- `product` — Product records
- `course` — Course records
- `certification` — Certification records

**Mapping Apps** — manage relational mappings between entities:

- `vendor_product_mapping` — Links Vendors to Products
- `product_course_mapping` — Links Products to Courses
- `course_certification_mapping` — Links Courses to Certifications

Each app is self-contained and follows the same internal structure, making it easy to extend, test, or replace independently.

---

## ✨ Features

- **Modular Django Apps** — Each entity and mapping is encapsulated in its own app, following Django best practices for large-scale projects.
- **CRUD APIs using `APIView`** — All create, read, update, and delete operations are implemented explicitly using `APIView`, with no reliance on DRF shortcuts.
- **Mapping Relationship Management** — Full support for managing many-to-many-style mappings between entities, including validation to prevent duplicates and enforce constraints.
- **Robust Validation Rules** — Custom validation is applied at the serializer and view level to enforce business logic (see [Validation Rules](#validation-rules)).
- **Query Parameter Filtering** — List endpoints support filtering by related entity IDs via query parameters.
- **Swagger & ReDoc Documentation** — Interactive API documentation is automatically generated via `drf-yasg` and available at `/swagger/` and `/redoc/`.
- **Clean REST Architecture** — Follows RESTful conventions: proper HTTP methods, appropriate status codes, and consistent JSON response structures.
- **Django Admin Integration** — All models are registered with the Django admin panel for easy data inspection and management during development.

---

## ✅ Validation Rules

The following validation rules are enforced across the API:

### Master Entities

| Rule                    | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Required Fields**     | All mandatory fields (e.g., `name`, `code`) must be present in the request |
| **Unique Code**         | Each master entity must have a globally unique `code` field                 |

### Mapping Entities

| Rule                          | Description                                                                            |
|-------------------------------|----------------------------------------------------------------------------------------|
| **Duplicate Mapping Prevention** | The same parent-child combination cannot be mapped more than once                  |
| **Valid Foreign Key Checks**  | The referenced parent and child entity IDs must exist in the database                  |
| **Single Primary Mapping**    | Only one mapping per parent entity can be marked as `is_primary = True`                |

These rules ensure data integrity and prevent inconsistencies in the mapping relationships.

---

## 🔌 API Endpoints

All endpoints return and accept **JSON**. Standard HTTP status codes are used throughout.

---

### Vendor APIs

| Method   | Endpoint              | Description              |
|----------|-----------------------|--------------------------|
| `GET`    | `/api/vendors/`       | List all vendors         |
| `POST`   | `/api/vendors/`       | Create a new vendor      |
| `GET`    | `/api/vendors/{id}/`  | Retrieve a vendor by ID  |
| `PUT`    | `/api/vendors/{id}/`  | Full update of a vendor  |
| `PATCH`  | `/api/vendors/{id}/`  | Partial update of a vendor |
| `DELETE` | `/api/vendors/{id}/`  | Delete a vendor          |

---

### Product APIs

| Method   | Endpoint               | Description               |
|----------|------------------------|---------------------------|
| `GET`    | `/api/products/`       | List all products         |
| `POST`   | `/api/products/`       | Create a new product      |
| `GET`    | `/api/products/{id}/`  | Retrieve a product by ID  |
| `PUT`    | `/api/products/{id}/`  | Full update of a product  |
| `PATCH`  | `/api/products/{id}/`  | Partial update of a product |
| `DELETE` | `/api/products/{id}/`  | Delete a product          |

---

### Course APIs

| Method   | Endpoint              | Description              |
|----------|-----------------------|--------------------------|
| `GET`    | `/api/courses/`       | List all courses         |
| `POST`   | `/api/courses/`       | Create a new course      |
| `GET`    | `/api/courses/{id}/`  | Retrieve a course by ID  |
| `PUT`    | `/api/courses/{id}/`  | Full update of a course  |
| `PATCH`  | `/api/courses/{id}/`  | Partial update of a course |
| `DELETE` | `/api/courses/{id}/`  | Delete a course          |

---

### Certification APIs

| Method   | Endpoint                     | Description                    |
|----------|------------------------------|--------------------------------|
| `GET`    | `/api/certifications/`       | List all certifications        |
| `POST`   | `/api/certifications/`       | Create a new certification     |
| `GET`    | `/api/certifications/{id}/`  | Retrieve a certification by ID |
| `PUT`    | `/api/certifications/{id}/`  | Full update of a certification |
| `PATCH`  | `/api/certifications/{id}/`  | Partial update                 |
| `DELETE` | `/api/certifications/{id}/`  | Delete a certification         |

---

### Vendor → Product Mapping APIs

| Method   | Endpoint                          | Description                         |
|----------|-----------------------------------|-------------------------------------|
| `GET`    | `/api/vendor-product-mappings/`       | List all vendor-product mappings    |
| `POST`   | `/api/vendor-product-mappings/`       | Create a vendor-product mapping     |
| `GET`    | `/api/vendor-product-mappings/{id}/`  | Retrieve a mapping by ID            |
| `PUT`    | `/api/vendor-product-mappings/{id}/`  | Full update of a mapping            |
| `PATCH`  | `/api/vendor-product-mappings/{id}/`  | Partial update of a mapping         |
| `DELETE` | `/api/vendor-product-mappings/{id}/`  | Delete a mapping                    |

---

### Product → Course Mapping APIs

| Method   | Endpoint                           | Description                        |
|----------|------------------------------------|------------------------------------|
| `GET`    | `/api/product-course-mappings/`       | List all product-course mappings   |
| `POST`   | `/api/product-course-mappings/`       | Create a product-course mapping    |
| `GET`    | `/api/product-course-mappings/{id}/`  | Retrieve a mapping by ID           |
| `PUT`    | `/api/product-course-mappings/{id}/`  | Full update of a mapping           |
| `PATCH`  | `/api/product-course-mappings/{id}/`  | Partial update of a mapping        |
| `DELETE` | `/api/product-course-mappings/{id}/`  | Delete a mapping                   |

---

### Course → Certification Mapping APIs

| Method   | Endpoint                                   | Description                              |
|----------|--------------------------------------------|------------------------------------------|
| `GET`    | `/api/course-certification-mappings/`       | List all course-certification mappings   |
| `POST`   | `/api/course-certification-mappings/`       | Create a course-certification mapping    |
| `GET`    | `/api/course-certification-mappings/{id}/`  | Retrieve a mapping by ID                 |
| `PUT`    | `/api/course-certification-mappings/{id}/`  | Full update of a mapping                 |
| `PATCH`  | `/api/course-certification-mappings/{id}/`  | Partial update of a mapping              |
| `DELETE` | `/api/course-certification-mappings/{id}/`  | Delete a mapping                         |

---

## 🔍 Filtering

List endpoints support query parameter-based filtering. Use these to retrieve related records efficiently:

```
# Get all products for a specific vendor
GET /api/products/?vendor_id=1

# Get all courses linked to a specific product
GET /api/courses/?product_id=2

# Get all certifications linked to a specific course
GET /api/certifications/?course_id=3

# Get all product-course mappings for a specific product
GET /api/product-course-mappings/?product_id=2

# Get all vendor-product mappings for a specific vendor
GET /api/vendor-product-mappings/?vendor_id=1
```

---

## 📚 Swagger Documentation

Interactive API documentation is auto-generated using [`drf-yasg`](https://github.com/axnsan12/drf-yasg).

| Interface | URL        | Description                              |
|-----------|------------|------------------------------------------|
| Swagger UI | `/swagger/` | Interactive Swagger UI — test endpoints directly from the browser |
| ReDoc     | `/redoc/`  | Clean, readable API reference documentation |

Once the development server is running, visit:

```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```

---

## ⚙️ Installation Guide

Follow these steps to get the project running locally.

### Prerequisites

- Python 3.10 or higher
- `pip` and `venv`
- Git

---

### Step 1 — Clone the Repository

```bash
git clone <repo-url>
cd entity-mapping-api
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**On macOS / Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — (Optional) Create a Superuser

```bash
python manage.py createsuperuser
```

### Step 6 — Start the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

---

## 🚀 Running the Project

### Quick Start (All Steps at Once)

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd entity-mapping-api

# 2. Create & activate virtual environment
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) Create admin user
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

The server will be live at `http://127.0.0.1:8000/`

---

### Access the App

Once the server is running, you can access the following:

| Interface      | URL                                  |
|----------------|--------------------------------------|
| Admin Panel    | `http://127.0.0.1:8000/admin/`       |
| Swagger UI     | `http://127.0.0.1:8000/swagger/`     |
| ReDoc          | `http://127.0.0.1:8000/redoc/`       |
| API Root       | `http://127.0.0.1:8000/api/`         |

---

## 🧪 Example API Requests

### Create a Vendor

```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "code": "ACME001",
    "description": "A leading technology vendor"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Acme Corp",
  "code": "ACME001",
  "description": "A leading technology vendor",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Create a Product

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cloud Suite Pro",
    "code": "CSP001",
    "description": "Enterprise cloud management product"
  }'
```

---

### Create a Vendor → Product Mapping

```bash
curl -X POST http://127.0.0.1:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "is_primary": true
  }'
```

---

### Get All Products for a Vendor

```bash
curl -X GET "http://127.0.0.1:8000/api/products/?vendor_id=1"
```

---

### Retrieve a Single Vendor

```bash
curl -X GET http://127.0.0.1:8000/api/vendors/1/
```

---

### Update a Vendor (Partial)

```bash
curl -X PATCH http://127.0.0.1:8000/api/vendors/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description for Acme Corp"
  }'
```

---

### Delete a Vendor

```bash
curl -X DELETE http://127.0.0.1:8000/api/vendors/1/
```

---

## 🔮 Future Improvements

The following enhancements are planned or recommended for production readiness:

- **Authentication & Authorization** — Integrate JWT or token-based authentication using `djangorestframework-simplejwt`, with role-based access control.
- **Pagination** — Add paginated list responses using DRF's `PageNumberPagination` or `CursorPagination` to handle large datasets.
- **Caching** — Introduce response caching with Django's cache framework (Redis backend) for frequently accessed endpoints.
- **Automated Test Coverage** — Write unit and integration tests using `pytest-django` to cover views, serializers, and validation logic.
- **Dockerization** — Add a `Dockerfile` and `docker-compose.yml` to containerize the app for consistent development and deployment environments.
- **CI/CD Pipeline** — Set up GitHub Actions for automated testing, linting, and deployment on every push.
- **Soft Delete Support** — Replace hard deletes with soft deletes using a `is_active` flag to preserve data history.
- **Audit Logging** — Track who created or modified each record using `created_by` and `updated_by` fields with user tracking middleware.

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Built with ❤️ using Django REST Framework
</p>
