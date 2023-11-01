# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('staff_id', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'ext_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)
