from django.db import models
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_certifications"
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name="certification_courses"
    )

    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "course_certification_mapping"
        unique_together = ("course", "certification")

    def __str__(self):
        return f"{self.course.name} -> {self.certification.name}"
