from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email")
    ordering = ("email",)
    fieldsets = (("User Info", {"fields": ("username", "email", "password")}),)
    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)