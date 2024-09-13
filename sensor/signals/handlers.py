from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from sensor.models import Sensor, SensorBrand, SensorType

User = get_user_model()


@receiver(post_save, sender=SensorType)
@receiver(post_save, sender=SensorBrand)
@receiver(post_save, sender=Sensor)
def set_object_permissions(sender, instance, **kwargs):
    """Set object-level permissions"."""
    instance.set_object_permissions()


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    for model in [
        SensorType,
        SensorBrand,
        Sensor,
    ]:
        model.set_model_permissions()
