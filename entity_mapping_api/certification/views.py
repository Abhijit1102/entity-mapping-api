from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Certification
from .serializers import CertificationSerializer


class CertificationListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Certifications",
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):

        certifications = Certification.objects.filter(is_active=True)
        serializer = CertificationSerializer(certifications, many=True)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Create Certification",
        request_body=CertificationSerializer
    )
    def post(self, request):

        serializer = CertificationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class CertificationDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Certification.objects.get(pk=pk)
        except Certification.DoesNotExist:
            return None


    def get(self, request, pk):

        certification = self.get_object(pk)

        if not certification:
            return Response({"error": "Certification not found"}, status=404)

        serializer = CertificationSerializer(certification)

        return Response(serializer.data)


    def put(self, request, pk):

        certification = self.get_object(pk)

        if not certification:
            return Response({"error": "Certification not found"}, status=404)

        serializer = CertificationSerializer(certification, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    def patch(self, request, pk):

        certification = self.get_object(pk)

        if not certification:
            return Response({"error": "Certification not found"}, status=404)

        serializer = CertificationSerializer(certification, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    def delete(self, request, pk):

        certification = self.get_object(pk)

        if not certification:
            return Response({"error": "Certification not found"}, status=404)

        certification.delete()

        return Response(status=204)
