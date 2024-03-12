from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from guardian.shortcuts import assign_perm


class User(AbstractUser):
    """
    Implement a custom user model to add flexibility in the future.
    """

    pass


class PermissionsBase(models.Model):
    """Base model for models that require permissions."""

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    PERMISSIONS_LEVELS = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    permissions_level = models.CharField(
        max_length=8, choices=PERMISSIONS_LEVELS, default="private"
    )

    def set_permissions(self):
        """Set object-level permissions."""

        delete, change, view = _get_perm_codenames(self.__class__)

        # Maintainers and owner get all perms
        for perm in [delete, change, view]:
            assign_perm(perm, Group.objects.get(name="Maintainer"), self)
            assign_perm(perm, self.owner, self)

        # View permissions based on permissions level
        if self.permissions_level in ["public", "internal"]:
            for group in ["Read only", "Contributor"]:
                assign_perm(view, Group.objects.get(name=group), self)

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
    )
