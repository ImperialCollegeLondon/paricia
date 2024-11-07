from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from guardian.shortcuts import assign_perm, get_anonymous_user, remove_perm


class User(AbstractUser):
    """Custom user model.

    All users are given staff status and added to the standard group.

    """

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.username != settings.ANONYMOUS_USER_NAME:
            standard_group = Group.objects.get(name="Standard")
            standard_group.user_set.add(self)


class PermissionsBase(models.Model):
    """Base model for models that require permissions."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        help_text="Owner of the object.",
    )

    VISIBILITY_LEVELS = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    visibility = models.CharField(
        max_length=8,
        choices=VISIBILITY_LEVELS,
        default="private",
        null=False,
        blank=False,
        help_text="Visibility level of the object. WARNING: Changing this setting will "
        "affect the permissions of the object. If 'Public', all users will be able to "
        "view and associate the object with their own.",
    )

    def set_object_permissions(self):
        """Set object-level delete, change and view permissions."""
        delete, change, view, add = _get_perm_codenames(self.__class__)
        standard_group = Group.objects.get(name="Standard")
        anonymous_user = get_anonymous_user()

        # View permissions based on permissions level
        if self.visibility in ["public", "internal"]:
            assign_perm(view, standard_group, self)
            assign_perm(view, anonymous_user, self)
            if self.owner:
                remove_perm(view, self.owner, self)
        elif self.visibility == "private" and self.owner:
            remove_perm(view, standard_group, self)
            remove_perm(view, anonymous_user, self)
            if self.owner:
                assign_perm(view, self.owner, self)

        # Assign change and delete permissions for owner
        for perm in [change, delete]:
            remove_perm(perm, standard_group, self)
            remove_perm(perm, anonymous_user, self)
            if self.owner:
                assign_perm(perm, self.owner, self)

    @classmethod
    def set_model_permissions(cls):
        """Set model-level add permissions."""
        apply_add_permissions_to_standard_group(cls)

    class Meta:
        abstract = True


def _get_perm_codenames(model):
    """Helper function to get delete, change and view permission codenames for a
    given model.
    """
    return (
        f"delete_{model._meta.model_name}",
        f"change_{model._meta.model_name}",
        f"view_{model._meta.model_name}",
        f"add_{model._meta.model_name}",
    )


def apply_add_permissions_to_standard_group(model):
    """Apply model-level add permissions to the standard user group.

    Args:
        model (Model): Model to apply permissions to.

    """
    delete, change, view, add = _get_perm_codenames(model)
    standard_group = Group.objects.get(name="Standard")
    content_type = ContentType.objects.get_for_model(model)
    permission, created = Permission.objects.get_or_create(
        codename=add, content_type=content_type
    )
    standard_group.permissions.add(permission)
