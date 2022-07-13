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

from rest_framework import generics

import formatting.models as fmt
import formatting.serializers as serializers


class ExtensionList(generics.ListCreateAPIView):
    queryset = fmt.Extension.objects.all()
    serializer_class = serializers.ExtensionSerializer


class ExtensionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Extension.objects.all()
    serializer_class = serializers.ExtensionSerializer


class DelimiterList(generics.ListCreateAPIView):
    queryset = fmt.Delimiter.objects.all()
    serializer_class = serializers.DelimiterSerializer


class DelimiterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Delimiter.objects.all()
    serializer_class = serializers.DelimiterSerializer


class DateList(generics.ListCreateAPIView):
    queryset = fmt.Date.objects.all()
    serializer_class = serializers.DateSerializer


class DateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Date.objects.all()
    serializer_class = serializers.DateSerializer


class TimeList(generics.ListCreateAPIView):
    queryset = fmt.Time.objects.all()
    serializer_class = serializers.TimeSerializer


class TimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Time.objects.all()
    serializer_class = serializers.TimeSerializer


class FormatList(generics.ListCreateAPIView):
    queryset = fmt.Format.objects.all()
    serializer_class = serializers.FormatSerializer


class FormatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Format.objects.all()
    serializer_class = serializers.FormatSerializer


class ClassificationList(generics.ListCreateAPIView):
    queryset = fmt.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer


class ClassificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer


class AssociationList(generics.ListCreateAPIView):
    queryset = fmt.Association.objects.all()
    serializer_class = serializers.AssociationSerializer


class AssociationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = fmt.Association.objects.all()
    serializer_class = serializers.AssociationSerializer
