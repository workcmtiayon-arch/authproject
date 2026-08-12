from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "is_active", "is_email_verified", "is_staff")
    list_filter = ("is_active", "is_email_verified", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Verification e-mail", {"fields": ("is_email_verified",)}),
    )