from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_perms

from .models import User


class PermissionsBaseAdmin(GuardedModelAdmin):
    """Base admin class for models that require permissions."""

    foreign_key_fields: list[str] = []

    def has_add_permission(self, request):
        """Allow all authenticated users to add objects."""
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        """Check if the user has the correct permission to change the object."""
        if obj is not None:
            return f"change_{self.model}" in get_perms(request.user, obj)
        return True

    def has_delete_permission(self, request, obj=None):
        """Check if the user has the correct permission to delete the object."""
        if obj is not None:
            return f"delete_{self.model}" in get_perms(request.user, obj)
        return True

    def has_view_permission(self, request, obj=None):
        """Allow all users to view the object."""
        return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit the queryset for foreign key fields."""
        if db_field.name in self.foreign_key_fields:
            kwargs["queryset"] = _get_queryset(db_field.related_model, request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Check if the user has the correct permissions to save the object."""
        for field in self.foreign_key_fields:
            owner = getattr(obj, field).owner
            perm_level = getattr(obj, field).permissions_level
            if owner != request.user and perm_level == "Private":
                raise PermissionDenied(f"Private {field}: Only owner can use.")
        super().save_model(request, obj, form, change)


def _get_queryset(model, user):
    """Return a queryset based on the permissions of the user.

    Returns all public objects plus any objects owned by the user.

    """
    return model.objects.filter(Q(owner=user) | Q(permissions_level="Public"))


class CustomUserAdmin(UserAdmin):
    """A slightly more restrictive user admin page."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
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
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        # Prevent changing permissions without using groups
        if not is_superuser:
            disabled_fields |= {
                "is_superuser",
                "is_staff",
                "user_permissions",
            }
        # Prevent users changing own permissions
        if not is_superuser and obj is not None and obj == request.user:
            disabled_fields |= {
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(User, CustomUserAdmin)
