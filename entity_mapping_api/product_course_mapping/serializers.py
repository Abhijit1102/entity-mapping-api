from rest_framework import serializers
from .models import ProductCourseMapping
from product.models import Product
from course.models import Course


class ProductCourseMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCourseMapping
        fields = ["id", "product", "course", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        product = data.get("product")
        course = data.get("course")
        is_primary = data.get("is_primary", False)
        instance = self.instance

        # Duplicate mapping check (on create)
        if instance is None:
            if ProductCourseMapping.objects.filter(product=product, course=course).exists():
                raise serializers.ValidationError(
                    "A mapping between this product and course already exists."
                )

        # Single primary mapping per product
        if is_primary:
            qs = ProductCourseMapping.objects.filter(product=product, is_primary=True)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "A primary mapping for this product already exists."
                )

        return data
