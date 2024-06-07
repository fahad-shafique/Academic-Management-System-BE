from rest_framework import serializers
from .models import User, Department, Degree, Parent, Student, Faculty, Role, Permission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'title',
            'profile_picture', 'gender', 'nationality', 'religion', 'date_of_birth',
            'blood_group', 'phone_number', 'secondary_phone_number', 'current_address',
            'permanent_address', 'user_type', 'is_active', 'is_staff', 'matriculation_number',
            'matriculation_board', 'school', 'intermediate_number', 'college', 'intermediate_board',
            'previous_degree'
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['dept_id', 'dept_code', 'department_name']


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ['degree_id', 'degree_name', 'department']


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['user']


class StudentSerializer(serializers.ModelSerializer):
    degree = DegreeSerializer()
    department = DepartmentSerializer()
    parents = ParentSerializer(many=True)

    class Meta:
        model = Student
        fields = [
            'user', 'sap_id', 'admission_year', 'status', 'graduation_year',
            'registration_date', 'registered_by', 'degree', 'department', 'parents'
        ]


class FacultySerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Faculty
        fields = ['user', 'faculty_id', 'faculty_code', 'is_director', 'is_hod', 'department']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']


class PermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Permission
        fields = ['permission_id', 'role', 'department', 'permission_field', 'can_view', 'can_edit', 'can_delete',
                  'can_create']
