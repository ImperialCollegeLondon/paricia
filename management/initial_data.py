from django.contrib.auth.models import Group


def create_user_group(apps, schema_editor):
    """Create the standard user group
    This function is run in migrations/0002_initial_data.py as an initial
    data migration at project initialization.
    """
    Group.objects.create(name="Standard")
