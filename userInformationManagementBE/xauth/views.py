from datetime import date

from django.db.models import F, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Student, Faculty, Department, Parent, Permission, Degree
from .serializers import UserSerializer, StudentSerializer, FacultySerializer, DepartmentSerializer, ParentSerializer, \
    DegreeSerializer, StudentListSerializer


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

    def post(self, request):
        user_type = request.user.user_type
        if not user_type == 'admin':
            return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            if pk is not None:
                user_id = pk
            else:
                user_id = request.user.id
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user_type = request.user.user_type
            if not user_type == 'admin':
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            user_to_update = User.objects.get(pk=pk)
            serializer = UserSerializer(user_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user_type = request.user.user_type
            if not user_type == 'admin':
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

            user_to_delete = User.objects.get(pk=pk)
            user_to_delete.delete()  # Delete the user
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class StudentViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating student information.
    """

    def post(self, request):
        user_type = request.user.user_type
        if not user_type == 'admin':
            return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        student_serializer = StudentSerializer(data=request.data)

        if student_serializer.is_valid():
            student_serializer.save()
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)

        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentListSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            request.data['degree'] = Degree.objects.get(degree_name=request.data['degree']).degree_id
            request.data['department'] = Department.objects.get(department_name=request.data['department']).dept_id
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user_type = request.user.user_type
            if not user_type == 'admin':
                return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FacultyViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating faculty information.
    """

    def post(self, request):
        user_type = request.user.user_type
        if not user_type == 'admin':
            return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        faculty_serializer = FacultySerializer(data=request.data)

        if faculty_serializer.is_valid():
            faculty_serializer.save()
            return Response(faculty_serializer.data, status=status.HTTP_201_CREATED)

        return Response(faculty_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            serializer = FacultySerializer(faculty, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Faculty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            faculty = Faculty.objects.get(pk=pk)
            faculty.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Faculty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DepartmentViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating department information.
    """

    def post(self, request):
        user_type = request.user.user_type
        if not user_type == 'admin':
            return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        department_serializer = DepartmentSerializer(data=request.data)

        if department_serializer.is_valid():
            department_serializer.save()
            return Response(department_serializer.data, status=status.HTTP_201_CREATED)

        return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            department = Department.objects.get(pk=pk)
            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ParentViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving and updating parent information.
    """

    def post(self, request):
        user_type = request.user.user_type
        if not user_type == 'admin':
            return Response({"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        parent_serializer = ParentSerializer(data=request.data)

        if parent_serializer.is_valid():
            parent_serializer.save()
            return Response(parent_serializer.data, status=status.HTTP_201_CREATED)

        return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            serializer = ParentSerializer(parent, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Parent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            parent = Parent.objects.get(pk=pk)
            parent.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Parent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DegreeListView(generics.ListAPIView):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    permission_classes = [IsAuthenticated]


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class StudentListView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return Student.objects.filter(user=user)
        elif user.user_type == 'parent':
            return Student.objects.filter(parent=user)
        elif user.user_type == 'admin' or user.user_type == 'faculty':
            return Student.objects.all()
        return Student.objects.none()

class DashboardStatsView(APIView):
    def get(self, request):
        total_students = Student.objects.count()
        total_departments = Department.objects.count()
        total_degrees = Degree.objects.count()

        # Calculate graduation rate
        current_year = date.today().year
        start_year = current_year - 5

        graduation_rates = []

        # Loop through the past five years
        for year in range(start_year, current_year + 1):
            # Graduated students for the specific year
            graduated_students = Student.objects.filter(
                graduation_year=year,  # Specific admission year
                graduation_year__lte=F('admission_year') + F('degree__completion_period')  # Graduated on time
            ).count()

            # Not graduated students for the specific year
            not_graduated_students = Student.objects.filter(
                admission_year=year,  # Specific admission year
            ).filter(
                Q(graduation_year__isnull=True) |  # Not graduated
                Q(graduation_year__gt=F('admission_year') + F('degree__completion_period'))  # Took too long
            ).count()

            # Total students for the year
            total_student = graduated_students + not_graduated_students

            # Calculate the graduation rate
            graduation_rate = (
                (graduated_students / total_student) * 100 if total_student > 0 else 0
            )

            # Append the result to the list
            graduation_rates.append({
                "year": year,
                "graduation_rate": round(graduation_rate, 2),
                "graduated_students": graduated_students,
                "not_graduated_students": not_graduated_students,
                "total_students": total_student,
            })

        data = {
            "total_students": total_students,
            "total_departments": total_departments,
            "total_degrees": total_degrees,
            "graduation_rate": graduation_rates,
        }
        return Response(data)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
