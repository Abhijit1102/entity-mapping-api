# 🗃️ MODEL_DESIGN.md — Entity Mapping API

> Database schema, entity relationships, and data integrity rules for the **Entity Mapping API** Django REST Framework backend.

---

## 📌 Table of Contents

- [System Overview](#1-system-overview)
- [Master Entity Models](#2-master-entity-models)
- [Mapping Models](#3-mapping-models)
- [Entity Relationship Diagram](#4-entity-relationship-diagram)
- [Relationship Explanation](#5-relationship-explanation)
- [Data Integrity Rules](#6-data-integrity-rules)
- [Example Data Flow](#7-example-data-flow)

---

## 1. System Overview

The **Entity Mapping API** is a modular backend system that manages a set of independent **master entities** and connects them through dedicated **mapping tables**.

Rather than using direct many-to-many fields, the system uses explicit **intermediate mapping models**. Each mapping model is its own Django app, carrying additional metadata such as `is_primary` and `is_active`, enabling fine-grained control over relationships.

```
Master Entities      →      Mapping Tables      →      Related Entities
─────────────────────────────────────────────────────────────────────────
Vendor               →   VendorProductMapping   →   Product
Product              →   ProductCourseMapping   →   Course
Course               →  CourseCertificationMapping  →  Certification
```

---

## 2. Master Entity Models

All four master entities — **Vendor**, **Product**, **Course**, and **Certification** — share an identical base field structure.

### 2.1 Shared Field Schema

| Field         | Django Type                 | Constraints          | Description                            |
| ------------- | --------------------------- | -------------------- | -------------------------------------- |
| `id`          | `AutoField`                 | Primary Key          | Auto-incremented unique identifier     |
| `name`        | `CharField(max_length=255)` | Required             | Human-readable name of the entity      |
| `code`        | `CharField(max_length=100)` | Required, Unique     | Short unique code for the entity       |
| `description` | `TextField`                 | Optional, Blank      | Long-form description                  |
| `is_active`   | `BooleanField`              | Default: `True`      | Soft delete flag                       |
| `created_at`  | `DateTimeField`             | Auto, `auto_now_add` | Timestamp when record was created      |
| `updated_at`  | `DateTimeField`             | Auto, `auto_now`     | Timestamp when record was last updated |

---

### 2.2 Example: Vendor Model

```python
from django.db import models


class Vendor(models.Model):
    name        = models.CharField(max_length=255)
    code        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendor"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.code})"
```

> The same structure applies to `Product`, `Course`, and `Certification` models — each in their own separate Django app.

---

### 2.3 Master Entity Summary

| App             | Model           | Table Name      |
| --------------- | --------------- | --------------- |
| `vendor`        | `Vendor`        | `vendor`        |
| `product`       | `Product`       | `product`       |
| `course`        | `Course`        | `course`        |
| `certification` | `Certification` | `certification` |

---

## 3. Mapping Models

Mapping models serve as **explicit junction tables** between master entities. Each mapping model lives in its own Django app and carries metadata about the relationship.

### 3.1 Shared Mapping Field Schema

| Field           | Django Type     | Constraints          | Description                                      |
| --------------- | --------------- | -------------------- | ------------------------------------------------ |
| `id`            | `AutoField`     | Primary Key          | Auto-incremented unique identifier               |
| `<parent>` (FK) | `ForeignKey`    | Required, `CASCADE`  | Reference to the parent entity                   |
| `<child>` (FK)  | `ForeignKey`    | Required, `CASCADE`  | Reference to the child entity                    |
| `is_primary`    | `BooleanField`  | Default: `False`     | Marks this as the primary mapping for the parent |
| `is_active`     | `BooleanField`  | Default: `True`      | Soft delete flag                                 |
| `created_at`    | `DateTimeField` | Auto, `auto_now_add` | Timestamp when mapping was created               |
| `updated_at`    | `DateTimeField` | Auto, `auto_now`     | Timestamp when mapping was last updated          |

---

### 3.2 Example: VendorProductMapping Model

```python
from django.db import models
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(models.Model):
    vendor     = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_products")
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_vendors")
    is_primary = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendor_product_mapping"
        unique_together = ("vendor", "product")  # Prevent duplicate mappings
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.vendor.name} → {self.product.name}"
```

---

### 3.3 Example: ProductCourseMapping Model

```python
from django.db import models
from product.models import Product
from course.models import Course


class ProductCourseMapping(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_courses")
    course     = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_products")
    is_primary = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_course_mapping"
        unique_together = ("product", "course")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} → {self.course.name}"
```

---

### 3.4 Example: CourseCertificationMapping Model

```python
from django.db import models
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(models.Model):
    course         = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_certifications")
    certification  = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name="certification_courses")
    is_primary     = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "course_certification_mapping"
        unique_together = ("course", "certification")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.course.name} → {self.certification.name}"
```

---

### 3.5 Mapping Entity Summary

| App                            | Model                        | Table Name                     | Relationship           |
| ------------------------------ | ---------------------------- | ------------------------------ | ---------------------- |
| `vendor_product_mapping`       | `VendorProductMapping`       | `vendor_product_mapping`       | Vendor → Product       |
| `product_course_mapping`       | `ProductCourseMapping`       | `product_course_mapping`       | Product → Course       |
| `course_certification_mapping` | `CourseCertificationMapping` | `course_certification_mapping` | Course → Certification |

---

## 4. Entity Relationship Diagram

### 4.1 Vertical Diagram

```
┌──────────┐
│  Vendor  │
└────┬─────┘
     │  ForeignKey
     ▼
┌──────────────────────┐
│  VendorProductMapping │  (is_primary, is_active)
└────────┬─────────────┘
         │  ForeignKey
         ▼
┌──────────┐
│  Product │
└────┬─────┘
     │  ForeignKey
     ▼
┌──────────────────────┐
│  ProductCourseMapping │  (is_primary, is_active)
└────────┬─────────────┘
         │  ForeignKey
         ▼
┌────────┐
│ Course │
└───┬────┘
    │  ForeignKey
    ▼
┌────────────────────────────┐
│ CourseCertificationMapping │  (is_primary, is_active)
└────────────┬───────────────┘
             │  ForeignKey
             ▼
┌───────────────┐
│ Certification │
└───────────────┘
```

---

### 4.2 Horizontal Diagram

```
Vendor  ──►  VendorProductMapping  ──►  Product  ──►  ProductCourseMapping  ──►  Course  ──►  CourseCertificationMapping  ──►  Certification
```

---

### 4.3 Full Schema Overview

```
vendor                      vendor_product_mapping         product
──────────────────          ──────────────────────         ──────────────────────
id (PK)             ◄──FK── vendor_id (FK)                 id (PK)
name                        product_id (FK) ──────────►    name
code (unique)               is_primary                     code (unique)
description                 is_active                      description
is_active                   created_at                     is_active
created_at                  updated_at                     created_at
updated_at                                                 updated_at

product                     product_course_mapping         course
──────────────────          ──────────────────────         ──────────────────────
id (PK)             ◄──FK── product_id (FK)                id (PK)
...                         course_id (FK) ──────────►     name
                            is_primary                     code (unique)
                            is_active                      description
                            created_at                     is_active
                            updated_at                     created_at
                                                           updated_at

course                      course_certification_mapping   certification
──────────────────          ────────────────────────────   ──────────────────────
id (PK)             ◄──FK── course_id (FK)                 id (PK)
...                         certification_id (FK) ──────►  name
                            is_primary                     code (unique)
                            is_active                      description
                            created_at                     is_active
                            updated_at                     created_at
                                                           updated_at
```

---

## 5. Relationship Explanation

### 5.1 Vendor → Product (`Many-to-Many via VendorProductMapping`)

```
Vendor (1) ──────────────────────► (*) VendorProductMapping (*) ◄──────────────────────── (1) Product
```

A single **Vendor** can be mapped to many **Products**, and a single **Product** can be associated with many **Vendors**. The mapping table manages this relationship explicitly, allowing metadata like `is_primary` to be stored per relationship.

---

### 5.2 Product → Course (`Many-to-Many via ProductCourseMapping`)

```
Product (1) ──────────────────────► (*) ProductCourseMapping (*) ◄──────────────────────── (1) Course
```

A **Product** can offer many **Courses**, and a **Course** can belong to many **Products**. The `is_primary` flag identifies the main course for a given product.

---

### 5.3 Course → Certification (`Many-to-Many via CourseCertificationMapping`)

```
Course (1) ──────────────────────► (*) CourseCertificationMapping (*) ◄──────────────────────── (1) Certification
```

A **Course** can lead to many **Certifications**, and a **Certification** can be linked to multiple **Courses**. The mapping tracks which certification is the primary outcome for a course.

---

### 5.4 Cardinality Summary

| Relationship           | Type         | Mapping Table                |
| ---------------------- | ------------ | ---------------------------- |
| Vendor ↔ Product       | Many-to-Many | `VendorProductMapping`       |
| Product ↔ Course       | Many-to-Many | `ProductCourseMapping`       |
| Course ↔ Certification | Many-to-Many | `CourseCertificationMapping` |

---

## 6. Data Integrity Rules

The following rules are enforced at the model, serializer, and/or database level to guarantee data consistency.

### 6.1 Master Entity Rules

| Rule                | Enforcement Level     | Details                                                                                |
| ------------------- | --------------------- | -------------------------------------------------------------------------------------- |
| **Unique `code`**   | Database + Serializer | `code` field has `unique=True`. Duplicate codes are rejected with a `400 Bad Request`. |
| **Required Fields** | Serializer validation | `name` and `code` are mandatory. Missing fields return validation errors.              |
| **Soft Delete**     | Application level     | Records are never hard-deleted. `is_active=False` marks a record as inactive.          |

---

### 6.2 Mapping Entity Rules

| Rule                              | Enforcement Level                         | Details                                                                                                                                                            |
| --------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Duplicate Mapping Prevention**  | Database (`unique_together`) + Serializer | The same `(parent, child)` combination cannot be mapped more than once.                                                                                            |
| **Valid Foreign Key Enforcement** | Database + Serializer                     | Parent and child IDs must reference existing records. Invalid IDs return `400 Bad Request`.                                                                        |
| **Single Primary Mapping**        | Serializer / View logic                   | Only one mapping per parent entity can have `is_primary=True`. Creating a new primary mapping automatically unsets any existing one, or raises a validation error. |
| **Soft Delete**                   | Application level                         | Mappings use `is_active=False` instead of deletion to preserve historical data.                                                                                    |

---

### 6.3 Database-Level Constraints Summary

```python
# Example: unique_together constraint on VendorProductMapping
class Meta:
    unique_together = ("vendor", "product")

# Example: unique code field on master entities
code = models.CharField(max_length=100, unique=True)
```

---

## 7. Example Data Flow

The system follows a top-down hierarchical data flow. Entities at each level are connected through their respective mapping tables.

### 7.1 Data Flow Diagram

```
 ┌─────────────┐
 │   Vendor    │  A vendor is registered in the system
 └──────┬──────┘
        │  creates / maps to
        ▼
 ┌─────────────┐
 │   Product   │  A vendor offers one or more products
 └──────┬──────┘
        │  creates / maps to
        ▼
 ┌─────────────┐
 │   Course    │  A product delivers one or more courses
 └──────┬──────┘
        │  creates / maps to
        ▼
 ┌───────────────┐
 │ Certification │  A course awards one or more certifications
 └───────────────┘
```

---

### 7.2 Narrative Flow

```
Vendor  ──creates──►  Product  ──offers──►  Course  ──provides──►  Certification
```

1. A **Vendor** is created and assigned a unique code.
2. **Products** are created and linked to one or more Vendors via `VendorProductMapping`.
3. **Courses** are created and linked to one or more Products via `ProductCourseMapping`.
4. **Certifications** are created and linked to one or more Courses via `CourseCertificationMapping`.
5. Each mapping records whether the relationship is the **primary** one (`is_primary=True`) and whether it is currently **active** (`is_active=True`).

---

### 7.3 Sample Data Trace

| Step | Action                                                 | Table Affected                 |
| ---- | ------------------------------------------------------ | ------------------------------ |
| 1    | Create Vendor `"Acme Corp"` (code: `ACME`)             | `vendor`                       |
| 2    | Create Product `"Cloud Suite"` (code: `CS01`)          | `product`                      |
| 3    | Map Acme → Cloud Suite (`is_primary=True`)             | `vendor_product_mapping`       |
| 4    | Create Course `"Cloud Fundamentals"` (code: `CF01`)    | `course`                       |
| 5    | Map Cloud Suite → Cloud Fundamentals                   | `product_course_mapping`       |
| 6    | Create Certification `"AWS Certified"` (code: `AWS01`) | `certification`                |
| 7    | Map Cloud Fundamentals → AWS Certified                 | `course_certification_mapping` |

---

_This document describes the current database schema and design decisions for the Entity Mapping API. Update this file whenever models are added, modified, or deprecated._
