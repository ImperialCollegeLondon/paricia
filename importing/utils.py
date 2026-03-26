def create_default_origins(apps, schema_editor):
    """Creates the default origins for data import."""
    ImportOrigin = apps.get_model("importing", "ImportOrigin")

    origins = ["file", "api", "Thingsboard"]
    for origin in origins:
        ImportOrigin.objects.create(origin=origin)


def remove_default_origins(apps, schema_editor):
    """Removes the default origins for data import."""
    ImportOrigin = apps.get_model("importing", "ImportOrigin")

    origins = ["file", "api", "Thingsboard"]
    for origin in origins:
        ImportOrigin.objects.filter(origin=origin).delete()
