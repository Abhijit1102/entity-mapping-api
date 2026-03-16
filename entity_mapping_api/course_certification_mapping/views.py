from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CourseCertificationMappingListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Course Certification Mappings",
        operation_description="Retrieve all course-certification mappings with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="Filter by course ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "certification_id",
                openapi.IN_QUERY,
                description="Filter by certification ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):

        course_id = request.query_params.get("course_id")
        certification_id = request.query_params.get("certification_id")

        mappings = CourseCertificationMapping.objects.all()

        if course_id:
            mappings = mappings.filter(course_id=course_id)

        if certification_id:
            mappings = mappings.filter(certification_id=certification_id)

        serializer = CourseCertificationMappingSerializer(mappings, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Course Certification Mapping",
        operation_description="Create a new mapping between a course and a certification",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer}
    )
    def post(self, request):

        serializer = CourseCertificationMappingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return CourseCertificationMapping.objects.get(pk=pk)
        except CourseCertificationMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Retrieve Course Certification Mapping",
        responses={200: CourseCertificationMappingSerializer}
    )
    def get(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = CourseCertificationMappingSerializer(mapping)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Course Certification Mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer}
    )
    def put(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Partial Update Course Certification Mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer}
    )
    def patch(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = CourseCertificationMappingSerializer(
            mapping,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Delete Course Certification Mapping",
        responses={204: "Mapping deleted"}
    )
    def delete(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        mapping.delete()

        return Response(status=204)
