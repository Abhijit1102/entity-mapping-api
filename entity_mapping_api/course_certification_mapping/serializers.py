from rest_framework import serializers
from .models import CourseCertificationMapping
from course.models import Course
from certification.models import Certification


class CourseCertificationMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCertificationMapping
        fields = ["id", "course", "certification", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        course = data.get("course")
        certification = data.get("certification")
        is_primary = data.get("is_primary", False)
        instance = self.instance

        # Duplicate mapping check (on create)
        if instance is None:
            if CourseCertificationMapping.objects.filter(
                course=course, certification=certification
            ).exists():
                raise serializers.ValidationError(
                    "A mapping between this course and certification already exists."
                )

        # Single primary mapping per course
        if is_primary:
            qs = CourseCertificationMapping.objects.filter(course=course, is_primary=True)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "A primary mapping for this course already exists."
                )

        return data
