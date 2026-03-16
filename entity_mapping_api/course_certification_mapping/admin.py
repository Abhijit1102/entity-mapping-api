from django.contrib import admin
from .models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ["id", "course", "certification", "is_primary", "created_at"]
    list_filter = ["is_primary"]
    search_fields = ["course__name", "course__code", "certification__name", "certification__code"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]
