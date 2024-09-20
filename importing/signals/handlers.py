from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from management.models import PermissionsBase

from ..models import DataImport
from ..tasks import ingest_data

User = get_user_model()


@receiver(post_save, sender=DataImport)
def set_object_permissions(sender, instance: PermissionsBase, **kwargs):
    """Set object-level permissions."""
    instance.set_object_permissions()


@receiver(post_save, sender=DataImport)
def process_data_ingestion(sender, instance: PermissionsBase, **kwargs):
    """Schedules the data ingestion task."""
    ingest_data(instance.pk)


@receiver(post_migrate)
def set_model_permissions(sender, **kwargs):
    """Set model-level permissions."""
    DataImport.set_model_permissions()
