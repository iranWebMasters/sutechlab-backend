from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Profile
class CustomUserAdmin(UserAdmin):
    model=User
    list_display=('email','is_superuser','is_active','last_login')
    list_filter=('email','is_superuser','is_active')
    search_fields=('email',)
    ordering=('email',)
    fieldsets = (
        ('authentication', {"fields": ("email", "password")}),
    )
    
    fieldsets = (
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile,)