from django.contrib import admin
from .models import VendorProductMapping


@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ["id", "vendor", "product", "is_primary", "created_at"]
    list_filter = ["is_primary"]
    search_fields = ["vendor__name", "vendor__code", "product__name", "product__code"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]
