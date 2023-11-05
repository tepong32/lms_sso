# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

from django.contrib import admin
from django.db import models
from .models import User, Profile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'is_active', 'is_staff', 'is_superuser',)
    
    # fieldsets = (
    #     (None, {'fields': ('staff_id', 'password')}),
    #     ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    #     ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    # )
    ### check how these can be modded
    ### commenting-them out made the admin page work


class ProfileAdmin(admin.ModelAdmin):

    list_display = ["last_name", "first_name", "ext_name", "middle_name",
        "classification", "department",
    ]  # Add 'classification' to the list_display


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(EmployeeClassification, EmployeeClassificationAdmin)
