from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VendorProductMappingListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Vendor Product Mappings",
        operation_description="Retrieve all vendor-product mappings with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "vendor_id",
                openapi.IN_QUERY,
                description="Filter by vendor ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="Filter by product ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):

        vendor_id = request.query_params.get("vendor_id")
        product_id = request.query_params.get("product_id")

        mappings = VendorProductMapping.objects.all()

        if vendor_id:
            mappings = mappings.filter(vendor_id=vendor_id)

        if product_id:
            mappings = mappings.filter(product_id=product_id)

        serializer = VendorProductMappingSerializer(mappings, many=True)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Create Vendor Product Mapping",
        operation_description="Create a new mapping between vendor and product",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer}
    )
    def post(self, request):

        serializer = VendorProductMappingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            return None


    @swagger_auto_schema(
        operation_summary="Retrieve Vendor Product Mapping",
        responses={200: VendorProductMappingSerializer}
    )
    def get(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = VendorProductMappingSerializer(mapping)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Update Vendor Product Mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer}
    )
    def put(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = VendorProductMappingSerializer(mapping, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    @swagger_auto_schema(
        operation_summary="Partial Update Vendor Product Mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer}
    )
    def patch(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = VendorProductMappingSerializer(
            mapping,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    @swagger_auto_schema(
        operation_summary="Delete Vendor Product Mapping",
        responses={204: "Mapping deleted"}
    )
    def delete(self, request, pk):

        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        mapping.delete()

        return Response(status=204)
