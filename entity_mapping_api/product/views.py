from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Products",
        operation_description="Retrieve all active products",
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):

        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Create Product",
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def post(self, request):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None


    @swagger_auto_schema(
        operation_summary="Retrieve Product",
        responses={200: ProductSerializer}
    )
    def get(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Update Product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def put(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    @swagger_auto_schema(
        operation_summary="Partial Update Product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def patch(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    @swagger_auto_schema(
        operation_summary="Delete Product",
        responses={204: "Product deleted"}
    )
    def delete(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response({"error": "Product not found"}, status=404)

        product.delete()

        return Response(status=204)
