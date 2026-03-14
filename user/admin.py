from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "status"
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "status",
    )

    ordering = ("name",)

    list_per_page = 20


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "department",
        "status",
        "is_staff"
    )

    list_filter = (
        "role",
        "status",
        "department",
        "is_staff"
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name"
    )

    ordering = ("username",)

    list_per_page = 20

    fieldsets = (

        ("Información de acceso", {
            "fields": ("username", "password")
        }),

        ("Información personal", {
            "fields": (
                "first_name",
                "last_name",
                "email"
            )
        }),

        ("Información organizacional", {
            "fields": (
                "role",
                "department",
                "status"
            )
        }),

        ("Permisos", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),

        ("Fechas importantes", {
            "fields": (
                "last_login",
                "date_joined"
            )
        }),

    )

    add_fieldsets = (

        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "first_name",
                "last_name",
                "role",
                "department",
                "status",
                "password1",
                "password2",
                "is_staff",
                "is_active"
            ),
        }),

    )