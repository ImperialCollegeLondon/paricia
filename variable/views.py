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

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response

import variable.models as var
import variable.serializers as serializers


class UnitList(generics.ListCreateAPIView):
    """
    List all units, or create a new unit.
    """

    queryset = var.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class UnitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a unit.
    """

    queryset = var.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class VariableList(generics.ListCreateAPIView):
    """
    List all variables, or create a new variable.
    """

    queryset = var.Variable.objects.all()
    serializer_class = serializers.VariableSerializer


class VariableDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a variable.
    """

    queryset = var.Variable.objects.all()
    serializer_class = serializers.VariableSerializer


class SensorInstallationList(generics.ListCreateAPIView):
    """
    List all sensor installations, or create a new sensor installation.
    """

    queryset = var.SensorInstallation.objects.all()
    serializer_class = serializers.SensorInstallationSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return serializers.SensorInstallationCreateSerializer
        return self.serializer_class





class SensorInstallationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a sensor installation.
    """

    queryset = var.SensorInstallation.objects.all()
    serializer_class = serializers.SensorInstallationSerializer


def get_limits(request):
    print(request.POST.get("variable_id"))
    id = int(request.POST.get("variable_id"))
    variable = var.Variable.objects.get(variable_id=id)
    data = {"maximum": variable.maximum, "minimum": variable.minimum}
    return JsonResponse(data)
