from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Student, Faculty, Department, Parent, Permission
from .serializers import UserSerializer, StudentSerializer, FacultySerializer, DepartmentSerializer, ParentSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['user_type'] = user.user_type

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/token',
        'api/token/refresh',
    ]
    return Response(routes)


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating user information.
    """

    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        try:
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user_permissions = Permission.objects.filter(role__role_name=request.user.user_type, department=user.department).first()
            if not user_permissions or not user_permissions.can_edit:
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StudentViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating student information.
    """

    def retrieve(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            user_permissions = Permission.objects.filter(role__role_name=request.user.user_type, department=student.department).first()
            if not user_permissions or not user_permissions.can_edit:
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FacultyViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating faculty information.
    """

    def retrieve(self, request, pk=None):
        try:
            faculty = Faculty.objects.get(pk=pk)
            serializer = FacultySerializer(faculty)
            return Response(serializer.data)
        except Faculty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            faculty = Faculty.objects.get(pk=pk)
            user_permissions = Permission.objects.filter(role__role_name=request.user.user_type, department=faculty.department).first()
            if not user_permissions or not user_permissions.can_edit:
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            serializer = FacultySerializer(faculty, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Faculty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DepartmentViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating department information.
    """

    def retrieve(self, request, pk=None):
        try:
            department = Department.objects.get(pk=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            department = Department.objects.get(pk=pk)
            user_permissions = Permission.objects.filter(role__role_name=request.user.user_type).first()
            if not user_permissions or not user_permissions.can_edit:
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ParentViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating parent information.
    """

    def retrieve(self, request, pk=None):
        try:
            parent = Parent.objects.get(pk=pk)
            serializer = ParentSerializer(parent)
            return Response(serializer.data)
        except Parent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            parent = Parent.objects.get(pk=pk)
            user_permissions = Permission.objects.filter(role__role_name=request.user.user_type).first()
            if not user_permissions or not user_permissions.can_edit:
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            serializer = ParentSerializer(parent, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Parent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
