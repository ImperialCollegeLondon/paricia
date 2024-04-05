from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

from .models import User


class PermissionsBaseAdmin(GuardedModelAdmin):
    """Base admin class for models that require permissions."""

    foreign_key_fields: list[str] = []
    limit_visibility_level = True  # limits standard users to creating private objects

    def has_add_permission(self, request):
        """Check if the user has the correct permission to add objects."""
        return request.user.has_perm(
            f"{self.opts.app_label}.add_{self.opts.model_name}"
        )

    def has_change_permission(self, request, obj=None):
        """Check if the user has the correct permission to change the object."""
        if obj is not None:
            return request.user.has_perm(
                f"{self.opts.app_label}.change_{self.opts.model_name}", obj
            )
        return True

    def has_delete_permission(self, request, obj=None):
        """Check if the user has the correct permission to delete the object."""
        if obj is not None:
            return request.user.has_perm(
                f"{self.opts.app_label}.delete_{self.opts.model_name}", obj
            )
        return True

    def has_view_permission(self, request, obj=None):
        """Check if the user has the correct permission to view the object."""
        if obj is not None:
            return request.user.has_perm(
                f"{self.opts.app_label}.view_{self.opts.model_name}", obj
            )
        return True

    def get_queryset(self, request):
        """Return a queryset of the objects that the user has view permissions for."""
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, f"{self.opts.app_label}.view_{self.opts.model_name}", qs
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit the queryset for foreign key fields."""
        if db_field.name in self.foreign_key_fields:
            kwargs["queryset"] = _get_queryset(db_field, request.user)
        if db_field.name == "owner":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Limit the queryset for choice fields."""
        if (
            db_field.name == "visibility"
            and self.limit_visibility_level
            and not request.user.is_superuser
        ):
            kwargs["initial"] = "private"
            kwargs["disabled"] = True
        return super().formfield_for_choice_field(db_field, request, **kwargs)


def _get_queryset(db_field, user):
    """Return a queryset based on the permissions of the user.

    Returns queryset of public objects and objects that the user has change permisions
    for.

    """
    app_name = db_field.related_model._meta.app_label
    model_name = db_field.related_model._meta.model_name
    user_objects = get_objects_for_user(user, f"{app_name}.change_{model_name}")
    public_objects = db_field.related_model.objects.filter(visibility="Public")
    return user_objects | public_objects


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
