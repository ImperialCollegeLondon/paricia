from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from variable.models import SensorInstallation, Unit, Variable

User = get_user_model()


@receiver(post_save, sender=SensorInstallation)
@receiver(post_save, sender=Unit)
@receiver(post_save, sender=Variable)
def set_object_permissions(sender, instance, **kwargs):
    """Set object-level permissions"."""
    instance.set_object_permissions()


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    for model in [
        SensorInstallation,
        Unit,
        Variable,
    ]:
        model.set_model_permissions()
