from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from measurement.models import Measurement, Report

User = get_user_model()



@receiver(post_save, sender=Measurement)
@receiver(post_save, sender=Report)
def set_permissions(sender, instance, **kwargs):
    """Set object-level permissions"."""
    # Get permissions for model
    delete, change, view = _get_perm_codenames(sender)

    # Assign change and delete permissions for owner
    for perm in [change, delete]:
        assign_perm(perm, instance.station.owner, instance)

    # Assign view permissions based on permissions level
    if instance.station.permissions_level == "public":
        for user in User.objects.all():
            assign_perm(view, user, instance)
    elif instance.station.permissions_level == "internal":
        for user in User.objects.filter(is_active=True):
            assign_perm(view, user, instance)
    else:  # private
        assign_perm(view, instance.station.owner, instance)


def _get_perm_codenames(model):
    """Helper function to get delete, change and view permission codenames for a
    given model.
    """
    return (
        f"delete_{model._meta.model_name}",
        f"change_{model._meta.model_name}",
        f"view_{model._meta.model_name}",
    )
