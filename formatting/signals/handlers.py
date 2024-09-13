from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from management.models import PermissionsBase

from ..models import (
    Classification,
    Date,
    Delimiter,
    Extension,
    Format,
    Time,
)

User = get_user_model()


@receiver(post_save, sender=Classification)
@receiver(post_save, sender=Date)
@receiver(post_save, sender=Delimiter)
@receiver(post_save, sender=Extension)
@receiver(post_save, sender=Format)
@receiver(post_save, sender=Time)
def set_object_permissions(sender, instance: PermissionsBase, **kwargs):
    """Set object-level permissions"."""
    instance.set_object_permissions()


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    for model in [
        Classification,
        Date,
        Delimiter,
        Extension,
        Format,
        Time,
    ]:
        model.set_model_permissions()
