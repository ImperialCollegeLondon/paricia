from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Implement a custom user model to add flexibility in the future.
    """

    pass


class PermissionsBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    PERMISSIONS_LEVELS = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    permissions_level = models.CharField(
        max_length=8, choices=PERMISSIONS_LEVELS, default="private"
    )

    class Meta:
        abstract = True
