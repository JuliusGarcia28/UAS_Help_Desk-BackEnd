from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'username',
        'email',
        'role',
        'status',
        'department',
        'is_staff',
        'is_superuser'
    )

    list_filter = (
        'role',
        'status',
        'department',
        'is_staff'
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": (
                "role",
                "status",
                "department"
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información adicional", {
            "fields": (
                "role",
                "status",
                "department"
            )
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)