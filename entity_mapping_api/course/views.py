from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List Courses",
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):

        courses = Course.objects.filter(is_active=True)
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Create Course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer}
    )
    def post(self, request):

        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None


    @swagger_auto_schema(
        operation_summary="Retrieve Course",
        responses={200: CourseSerializer}
    )
    def get(self, request, pk):

        course = self.get_object(pk)

        if not course:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseSerializer(course)

        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Update Course",
        request_body=CourseSerializer
    )
    def put(self, request, pk):

        course = self.get_object(pk)

        if not course:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    @swagger_auto_schema(
        operation_summary="Partial Update Course",
        request_body=CourseSerializer
    )
    def patch(self, request, pk):

        course = self.get_object(pk)

        if not course:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseSerializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    @swagger_auto_schema(
        operation_summary="Delete Course"
    )
    def delete(self, request, pk):

        course = self.get_object(pk)

        if not course:
            return Response({"error": "Course not found"}, status=404)

        course.delete()

        return Response(status=204)
