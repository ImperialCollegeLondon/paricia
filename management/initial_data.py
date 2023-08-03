from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group, Permission


def populate_groups(apps, schema_editor):
    """
    Create groups and assign their permissions.
    This function is run in migrations/0002_initial_data.py as an initial
    data migration at project initialization.
    Sets up some basic model-level permissions for different groups when the
    project is initialised.
    User manager: Full permissions over the management app to add, change, delete, view
    users.
    Maintainer: Full permissions over the "data apps" to add, change, delete, view
    data in the database, but not users.
    Contributor: Initially given add permissions for Measurement and Import apps.
    Read only: Given view permission for all apps other than "management".
    """
    # Create user groups
    user_roles = ["User manager", "Maintainer", "Contributor", "Read only"]
    for name in user_roles:
        Group.objects.create(name=name)

    # Permissions have to be created before applying them
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    # Assign model-level permissions to each group.
    all_perms = Permission.objects.all()

    # User managers
    user_manager_perms = [
        i for i in all_perms if i.content_type.app_label in ["management"]
    ]
    Group.objects.get(name="User manager").permissions.add(*user_manager_perms)

    # Maintainers
    maintainer_perms = [
        i for i in all_perms if i.content_type.app_label not in ["management"]
    ]
    Group.objects.get(name="Maintainer").permissions.add(*maintainer_perms)

    # Contributors
    contrib_perms = [i for i in maintainer_perms if i.codename.split("_")[0] in ["add"]]
    contrib_perms = [
        i
        for i in contrib_perms
        if i.content_type.app_label in ["measurement", "importing"]
    ]
    Group.objects.get(name="Contributor").permissions.add(*contrib_perms)

    # Read only
    read_only_perms = [
        i for i in all_perms if i.content_type.app_label not in ["management"]
    ]
    read_only_perms = [
        i for i in read_only_perms if i.codename.split("_")[0] in ["view"]
    ]
    Group.objects.get(name="Read only").permissions.add(*read_only_perms)
