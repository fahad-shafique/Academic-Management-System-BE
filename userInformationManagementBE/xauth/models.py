from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('parent', 'Parent'),
        ('alumni', 'Alumni'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    secondary_phone_number = models.CharField(max_length=15, blank=True)
    current_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    matriculation_number = models.CharField(max_length=50, blank=True)
    matriculation_board = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    intermediate_number = models.CharField(max_length=50, blank=True)
    college = models.CharField(max_length=100, blank=True)
    intermediate_board = models.CharField(max_length=100, blank=True)
    previous_degree = models.CharField(max_length=100, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_type']

    def __str__(self):
        return self.username


class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_code = models.CharField(max_length=10, unique=True)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


class Degree(models.Model):
    degree_id = models.AutoField(primary_key=True)
    degree_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.degree_name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - Parent"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sap_id = models.CharField(max_length=20, unique=True)
    admission_year = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    registration_date = models.DateField()
    registered_by = models.CharField(max_length=100)
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, related_name='primary_department', on_delete=models.CASCADE)
    parents = models.ManyToManyField(Parent)

    def __str__(self):
        return f"{self.user.username} - {self.sap_id}"


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_id = models.AutoField(primary_key=True)
    faculty_code = models.CharField(max_length=20, unique=True)
    is_director = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faculty_code} - {self.department.department_name}"


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name


class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    permission_field = models.CharField(max_length=50)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
