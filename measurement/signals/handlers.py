from django.db.models.signals import post_migrate
from django.dispatch import receiver

from measurement.models import Measurement, Report


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    for model in [
        Measurement,
        Report,
    ]:
        model.set_model_permissions()
