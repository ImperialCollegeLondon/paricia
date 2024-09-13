########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

from django.shortcuts import render
from django.views import View
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user

from station.models import Station


class DailyValidation(LoginRequiredMixin, View):
    """View for displaying the Daily Validation dash app."""

    def get(self, request, *args, **kwargs):
        from .dash_apps import daily_validation  # noqa

        stations = get_objects_for_user(request.user, "change_station", klass=Station)
        station_codes = list(stations.values_list("station_code", flat=True))
        context = {"django_context": {"stations_list": {"children": station_codes}}}
        return render(request, "daily_validation.html", context)


class DataReport(View):
    """View for displaying the Data Report dash app."""

    def get(self, request, *args, **kwargs):
        from .dash_apps import data_report  # noqa

        stations = get_objects_for_user(
            request.user, "view_measurements", klass=Station
        )
        station_codes = list(stations.values_list("station_code", flat=True))
        context = {"django_context": {"stations_list": {"children": station_codes}}}
        return render(request, "data_report.html", context)
