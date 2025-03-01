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
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


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

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        parent = Parent.objects.create(user=user, **validated_data)
        return parent

class StudentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    degree = DegreeSerializer()
    department = DepartmentSerializer()
    parents = ParentSerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student

class FacultySerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Faculty
        fields = ['user', 'faculty_id', 'faculty_code', 'is_director', 'is_hod', 'department']

    def create(self, validated_data):
        faculty = Faculty.objects.create(**validated_data)
        return faculty

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']

class StatsSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    total_degrees = serializers.IntegerField()
    graduation_rate = serializers.ListField(child=serializers.FloatField())

