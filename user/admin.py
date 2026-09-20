from django.contrib import admin
from user.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            _('Login'),
            {'fields': ('id', 'email', 'password')}
        ),
        (
            _('Personal Information'),
            {'fields': ('first_name', 'last_name')}
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "first_name", "last_name", "is_superuser")
    ordering = ("id", 'first_name', 'last_name')
    search_fields = ("first_name", "last_name", "email")

admin.site.register(Permission)