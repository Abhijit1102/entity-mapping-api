from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VendorListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Vendors",
        operation_description="Retrieve all active vendors",
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        vendors = Vendor.objects.filter(is_active=True)
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Vendor",
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer}
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Retrieve Vendor",
        responses={200: VendorSerializer}
    )
    def get(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=404)

        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update Vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer}
    )
    def put(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=404)

        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Partial Update Vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer}
    )
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=404)

        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Delete Vendor",
        responses={204: "Vendor deleted"}
    )
    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"error": "Vendor not found"}, status=404)

        vendor.delete()
        return Response(status=204)
