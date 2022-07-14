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

import variable.models as var
import variable.serializers as serializers


class UnitList(generics.ListCreateAPIView):
    queryset = var.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class UnitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = var.Unit.objects.all()
    serializer_class = serializers.UnitSerializer


class VariableList(generics.ListCreateAPIView):
    queryset = var.Variable.objects.all()
    serializer_class = serializers.VariableSerializer


class VariableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = var.Variable.objects.all()
    serializer_class = serializers.VariableSerializer


class SensorInstallationList(generics.ListCreateAPIView):
    queryset = var.SensorInstallation.objects.all()
    serializer_class = serializers.SensorInstallationSerializer


class SensorInstallationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = var.SensorInstallation.objects.all()
    serializer_class = serializers.SensorInstallationSerializer


def get_limits(request):
    print(request.POST.get("variable_id"))
    id = int(request.POST.get("variable_id"))
    variable = var.Variable.objects.get(variable_id=id)
    data = {"maximum": variable.maximum, "minimum": variable.minimum}
    return JsonResponse(data)
