# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

from django.contrib import admin
from django.db import models
from .models import User, EmployeeType, WorkGroup, Profile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'is_active', 'is_staff', 'is_superuser','last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('staff_id', 'password')}),
        ### these were removed because they're not attribute fields of Custom User
        # ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class BooleanListFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

class IsTeamLeaderFilter(BooleanListFilter):
    title = 'is team leader'
    parameter_name = 'is_team_leader'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(emp_type__name=EmployeeType.Type.TEAM_LEADER)
        elif value == 'no':
            return queryset.exclude(emp_type__name=EmployeeType.Type.TEAM_LEADER)

class IsOperationsManagerFilter(BooleanListFilter):
    title = 'is operations manager'
    parameter_name = 'is_operations_manager'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(emp_type__name=EmployeeType.Type.OPERATIONS_MGR)
        elif value == 'no':
            return queryset.exclude(emp_type__name=EmployeeType.Type.OPERATIONS_MGR)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["emp_type", "last_name", "first_name", "ext_name", "middle_name", 
    ]
    list_filter = (IsTeamLeaderFilter, IsOperationsManagerFilter)

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

class WorkGroupAdmin(admin.ModelAdmin):
    list_display = ['name']




admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(WorkGroup, WorkGroupAdmin)
