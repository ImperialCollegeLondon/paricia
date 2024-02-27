from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_perms

from .models import Sensor, SensorBrand, SensorType

admin.site.site_header = "Paricia Administration - Sensors"


class BaseAdmin(GuardedModelAdmin):
    foreign_key_fields: list[str] = []

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return f"change_{self.model}" in get_perms(request.user, obj)
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return f"delete_{self.model}" in get_perms(request.user, obj)
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.foreign_key_fields:
            kwargs["queryset"] = _get_queryset(db_field.related_model, request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        for field in self.foreign_key_fields:
            owner = getattr(obj, field).owner
            perm_level = getattr(obj, field).permissions_level
            if owner != request.user and perm_level == "Private":
                raise PermissionDenied(f"Private {field}: Only owner can use.")
        super().save_model(request, obj, form, change)


@admin.register(SensorType)
class SensorTypeAdmin(BaseAdmin):
    model = "sensortype"
    list_display = ["name", "type_id", "owner", "permissions_level"]


@admin.register(SensorBrand)
class SensorBrandAdmin(BaseAdmin):
    model = "sensorbrand"
    list_display = ["name", "brand_id", "owner", "permissions_level"]


@admin.register(Sensor)
class SensorAdmin(BaseAdmin):
    model = "sensor"
    list_display = [
        "sensor_id",
        "code",
        "model",
        "serial",
        "status",
        "owner",
        "permissions_level",
    ]
    list_filter = ["sensor_brand", "sensor_type"]
    foreign_key_fields = ["sensor_brand", "sensor_type"]


def _get_queryset(model, user):
    return model.objects.filter(Q(owner=user) | Q(permissions_level="Public"))
