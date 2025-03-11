from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from router import models, forms

# Register your models here.

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = models.User
    search_fields = ("email", "first_name", "last_name",)
    ordering = ("email", "first_name", "last_name",)
    list_display_links = ("email", "first_name", "last_name")
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", "is_superuser", "last_login")
    list_filter = ("email", "first_name", "last_name", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "password1", "password2", "is_staff",
                "is_active", "is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "first_name", "last_name",)
    ordering = ("email", "first_name", "last_name",)
    