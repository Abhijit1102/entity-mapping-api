from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
