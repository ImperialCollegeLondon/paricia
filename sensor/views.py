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

from __future__ import unicode_literals

from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from excel_response import ExcelResponse
from rest_framework import generics

import sensor.models as sens
import sensor.serializers as serializers


class SensorTypeList(generics.ListCreateAPIView):
    """
    List all sensor types, or create a new sensor type.
    """

    queryset = sens.SensorType.objects.all()
    serializer_class = serializers.SensorTypeSerializer


class SensorTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a sensor type.
    """

    queryset = sens.SensorType.objects.all()
    serializer_class = serializers.SensorTypeSerializer


class SensorBrandList(generics.ListCreateAPIView):
    """
    List all sensor brands, or create a new sensor brand.
    """

    queryset = sens.SensorBrand.objects.all()
    serializer_class = serializers.SensorBrandSerializer


class SensorBrandDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a sensor brand.
    """

    queryset = sens.SensorBrand.objects.all()
    serializer_class = serializers.SensorBrandSerializer


class SensorList(generics.ListCreateAPIView):
    """
    List all sensors, or create a new sensor.
    """

    queryset = sens.Sensor.objects.all()
    serializer_class = serializers.SensorSerializer


class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a sensor.
    """

    queryset = sens.Sensor.objects.all()
    serializer_class = serializers.SensorSerializer


@permission_required("sensor.view_sensor")
def export_sensor(request):
    if request.user.is_authenticated:
        header = [
            ["Code", "Type", "Brand", "Model", "Serial"],
        ]
        body = []
        objetos = sens.Sensor.objects.all()
        for objeto in objetos:
            row = []
            row.append(objeto.code)
            row.append(
                objeto.sensor_type.name if objeto.sensor_type is not None else None
            )
            row.append(
                objeto.sensor_brand.brand if objeto.sensor_brand is not None else None
            )
            row.append(objeto.model)
            row.append(objeto.serial)
            body.append(row)
        response = ExcelResponse(header + body, "iMHEA_sensors")
        return response


@permission_required("sensor.view_sensor")
def sensors_list(request):
    sensores = sens.Sensor.objects.all()
    slist = []
    for row in sensores:
        slist.append(
            row.code + " -- " + ("" if row.model is None else row.model + " - ")
        )
    return JsonResponse({"sensors_list": slist})
