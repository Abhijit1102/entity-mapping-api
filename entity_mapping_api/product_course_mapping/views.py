from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductCourseMappingListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Product Course Mappings",
        operation_description="Retrieve all product-course mappings with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="Filter by product ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="Filter by course ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):

        product_id = request.query_params.get("product_id")
        course_id = request.query_params.get("course_id")

        mappings = ProductCourseMapping.objects.all()

        if product_id:
            mappings = mappings.filter(product_id=product_id)

        if course_id:
            mappings = mappings.filter(course_id=course_id)

        serializer = ProductCourseMappingSerializer(mappings, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Product Course Mapping",
        operation_description="Create a new mapping between a product and a course",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer}
    )
    def post(self, request):

        serializer = ProductCourseMappingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return ProductCourseMapping.objects.get(pk=pk)
        except ProductCourseMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Retrieve Product Course Mapping",
        responses={200: ProductCourseMappingSerializer}
    )
    def get(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = ProductCourseMappingSerializer(mapping)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Product Course Mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer}
    )
    def put(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = ProductCourseMappingSerializer(mapping, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Partial Update Product Course Mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer}
    )
    def patch(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = ProductCourseMappingSerializer(
            mapping,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Delete Product Course Mapping",
        responses={204: "Mapping deleted"}
    )
    def delete(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        mapping.delete()

        return Response(status=204)
