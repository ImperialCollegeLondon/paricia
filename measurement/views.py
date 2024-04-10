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

from rest_framework import generics

import measurement.models as meas
import measurement.serializers as serializers


class MeasurementList(generics.ListAPIView):
    """
    List measurements of all types.

    This view is used to retrieve the measurement records filtering by station,
    variable, start_time, end_time, is_validated and is_active. If no parameters
    are provided, an empty queryset is returned.
    """

    model = meas.Measurement
    serializer_class = serializers.MeasurementSerializer

    def get_queryset(self):
        """Custom queryset to filter the results."""
        params = self.request.query_params
        options = {}
        if params.get("station_id"):
            options["station__station_id"] = params.get("station_id")
        if params.get("variable_id"):
            options["variable__variable_id"] = params.get("variable_id")
        if params.get("start_time"):
            options["time__gte"] = params.get("start_time")
        if params.get("end_time"):
            options["time__lte"] = params.get("end_time")
        if params.get("is_validated"):
            options["is_validated"] = params.get("is_validated")
        if params.get("is_active"):
            options["is_active"] = params.get("is_active")

        if not options:
            return self.model.objects.none()

        return self.model.objects.filter(**options)


class ReportList(generics.ListAPIView):
    """
    List all measurements of Report.

    This view is used to retrieve the results filtering by station, variable,
    report_type, start_time, and end_time. If no parameters are provided, an empty
    queryset is returned.
    """

    model = meas.Report
    serializer_class = serializers.ReportSerializer

    def get_queryset(self):
        """Custom queryset to filter the results."""
        params = self.request.query_params
        options = {}
        if params.get("station_id"):
            options["station__station_id"] = params.get("station_id")
        if params.get("variable_id"):
            options["variable__variable_id"] = params.get("variable_id")
        if params.get("report_type"):
            options["report_type"] = params.get("report_type")
        if params.get("start_time"):
            options["time__gte"] = params.get("start_time")
        if params.get("end_time"):
            options["time__lte"] = params.get("end_time")

        if not options:
            return self.model.objects.none()

        return self.model.objects.filter(**options)
