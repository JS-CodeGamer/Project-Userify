from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class MyUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'age', 'gender', 'is_admin', 'is_active',)
    list_filter = ('username', 'first_name', 'email', 'age', 'gender', 'user_category',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'middle_name', 'last_name', 'age', 'gender'),
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    ordering = ('email','username',)
    filter_horizontal = ()


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(OTPModel)
