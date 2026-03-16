from django.contrib import admin
from .models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "course", "is_primary", "created_at"]
    list_filter = ["is_primary"]
    search_fields = ["product__name", "product__code", "course__name", "course__code"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]
