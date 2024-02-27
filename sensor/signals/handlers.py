from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from sensor.models import Sensor

User = get_user_model()


@receiver(post_save, sender=Sensor)
def set_permissions(sender, instance, **kwargs):
    """Set object-level permissions"."""
    # Get permissions for model
    delete, change, view = _get_perm_codenames(sender)

    # Assign view permissions for all users
    assign_perm(view, User.objects.all(), instance)

    # Assign change and delete permissions for owner
    if instance.owner:
        for perm in [change, delete]:
            assign_perm(perm, instance.owner, instance)


def _get_perm_codenames(model):
    """Helper function to get delete, change and view permission codenames for a
    given model.
    """
    return (
        f"delete_{model._meta.model_name}",
        f"change_{model._meta.model_name}",
        f"view_{model._meta.model_name}",
    )
