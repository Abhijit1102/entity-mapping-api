from django.db import models
from product.models import Product
from course.models import Course


class ProductCourseMapping(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_courses"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_products"
    )

    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_course_mapping"
        unique_together = ("product", "course")

    def __str__(self):
        return f"{self.product.name} -> {self.course.name}"
