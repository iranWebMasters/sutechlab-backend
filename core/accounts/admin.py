from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "customer_code", "is_superuser", "is_active", "last_login")
    list_filter = ("is_superuser", "is_active")
    search_fields = ("email", "customer_code")
    ordering = ("email",)

    fieldsets = (
        ("Authentication Information", {"fields": ("email", "password")}),
        ("Customer Information", {"fields": ("customer_code",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
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
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "national_id",
        "phone_number",
        "address",
        "postal_code",
        "created_date",
        "updated_date",
    )
    search_fields = (
        "user__email",
        "first_name",
        "last_name",
        "national_id",
        "phone_number",
    )
    list_filter = ("created_date", "updated_date")
    ordering = ("user",)
    readonly_fields = ("created_date", "updated_date")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
