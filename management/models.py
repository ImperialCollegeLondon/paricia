from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from guardian.shortcuts import assign_perm, get_anonymous_user


class User(AbstractUser):
    """Custom user model.

    All users are given staff status and added to the standard group.

    """

    def save(self, *args, **kwargs):
        if self.username != "AnonymousUser":
            self.is_staff = True
        super().save(*args, **kwargs)
        if self.username != "AnonymousUser":
            standard_group = Group.objects.get(name="Standard")
            standard_group.user_set.add(self)


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
        standard_group = Group.objects.get(name="Standard")
        anonymous_user = get_anonymous_user()

        # View permissions based on permissions level
        if self.permissions_level in ["public", "internal"]:
            assign_perm(view, standard_group, self)
            assign_perm(view, anonymous_user, self)
        elif self.permissions_level == "private" and self.owner:
            assign_perm(view, self.owner, self)

        # Assign change and delete permissions for owner
        if self.owner:
            for perm in [change, delete]:
                assign_perm(perm, self.owner, self)

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
