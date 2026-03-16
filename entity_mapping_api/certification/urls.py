from django.urls import path
from .views import CertificationListCreateAPIView, CertificationDetailAPIView

urlpatterns = [
    path("", CertificationListCreateAPIView.as_view(), name="certification-list"),
    path("<int:pk>/", CertificationDetailAPIView.as_view(), name="certification-detail"),
]
