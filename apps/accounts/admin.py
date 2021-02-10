from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import User, Token
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.


@admin.register(User)
class AdminUser(UserAdmin):
    exclude = [
        "username",
    ]
    list_display = (
        "id",
        "created_at",
        "last_updated_at",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = ("created_at", "last_updated_at", "is_staff", "is_active")
    search_fields = ["first_name", "last_name", "email"]
    ordering = ("created_at", "last_updated_at", "is_staff", "is_active")
    exclude = ("username",)
    fieldsets = (
        ("Personal info", {"fields": ("first_name", "last_name", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


@admin.register(Token)
class AdminToken(admin.ModelAdmin):
    list_display = (
        "key",
        "user",
        "created",
    )
    list_filter = ("user",)
