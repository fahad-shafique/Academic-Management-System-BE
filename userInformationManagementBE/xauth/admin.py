from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User, Department, Degree, Student


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'user_type')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'title', 'profile_picture', 'gender', 'nationality', 'religion', 'date_of_birth',
            'blood_group', 'phone_number', 'secondary_phone_number', 'current_address', 'permanent_address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Department)
admin.site.register(Degree)
admin.site.register(Student)

