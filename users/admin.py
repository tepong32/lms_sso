# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

from django.contrib import admin
from django.db import models
from .models import User, WorkGroup, Profile, EmployeeClassification

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'is_active', 'is_staff', 'is_superuser','last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('staff_id', 'password')}),
        ### these were removed because they're not attribute fields of Custom User
        # ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    


class EmployeeClassificationAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProfileAdmin(admin.ModelAdmin):
    '''
        remove classification first when doing initial migrations to make way for the EmployeeClassification models to be created first.
        return it afterwards.
    '''
    list_display = ["last_name", "first_name", "ext_name", "middle_name", "classification", "department",
    ]  # Add 'classification' to the list_display


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(EmployeeClassification, EmployeeClassificationAdmin)
admin.site.register(WorkGroup)
