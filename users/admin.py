# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

from django.contrib import admin
from django.db import models
<<<<<<< HEAD
from .models import User, WorkGroup, WorkGroupName
=======
from .models import User#, WorkGroup, WorkGroupName
>>>>>>> master


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
            return queryset.filter(is_team_leader=True)
        elif value == 'no':
            return queryset.exclude(is_team_leader=True)

class IsOperationsManagerFilter(BooleanListFilter):
    title = 'is operations manager'
    parameter_name = 'is_operations_manager'

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(is_operations_manager=True)
        elif value == 'no':
            return queryset.exclude(is_operations_manager=True)

class CustomUserAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('staff_id', 'is_active', 'is_staff', 'is_superuser','last_login', 'date_joined')
    list_filter = (IsTeamLeaderFilter, IsOperationsManagerFilter)
    fieldsets = (
        (None, {'fields': ('staff_id', 'password', 'is_advisor', 'is_team_leader', 'is_operations_manager')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
=======
    list_display = ('staff_id', 'is_active', 'is_staff', 'is_superuser','last_login', 'date_joined', 'workgroup')
    list_filter = (IsTeamLeaderFilter, IsOperationsManagerFilter)
    fieldsets = (
        (None, {'fields': ('staff_id', 'password', 'is_advisor', 'is_team_leader', 'is_operations_manager', 'workgroup', 'groups')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
>>>>>>> master
    )








admin.site.register(User, CustomUserAdmin)
<<<<<<< HEAD
admin.site.register(WorkGroup)
admin.site.register(WorkGroupName)
=======
# admin.site.register(WorkGroup)
# admin.site.register(WorkGroupName)
>>>>>>> master
