# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

from django.contrib import admin
from django.db import models
from .models import User, Profile, EmployeeType, WorkGroup

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'is_active', 'is_staff', 'is_superuser','last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('staff_id', 'password')}),
        ### these were removed because they're not attribute fields of Custom User
        # ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "ext_name", "middle_name", "emp_type",
    ]


class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

class WorkGroupAdmin(admin.ModelAdmin):
    list_display = ['name']





admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(WorkGroup, WorkGroupAdmin)
