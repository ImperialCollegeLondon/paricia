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

import formatting.models as fmt
import formatting.serializers as serializers


class ExtensionList(generics.ListCreateAPIView):
    """List all extensions, or create a new extension."""

    queryset = fmt.Extension.objects.all()
    serializer_class = serializers.ExtensionSerializer


class ExtensionDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a extension."""

    queryset = fmt.Extension.objects.all()
    serializer_class = serializers.ExtensionSerializer


class DelimiterList(generics.ListCreateAPIView):
    """List all delimiters, or create a new delimiter."""

    queryset = fmt.Delimiter.objects.all()
    serializer_class = serializers.DelimiterSerializer


class DelimiterDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a delimiter."""

    queryset = fmt.Delimiter.objects.all()
    serializer_class = serializers.DelimiterSerializer


class DateList(generics.ListCreateAPIView):
    """List all dates, or create a new date."""

    queryset = fmt.Date.objects.all()
    serializer_class = serializers.DateSerializer


class DateDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a date."""

    queryset = fmt.Date.objects.all()
    serializer_class = serializers.DateSerializer


class TimeList(generics.ListCreateAPIView):
    """List all times, or create a new time."""

    queryset = fmt.Time.objects.all()
    serializer_class = serializers.TimeSerializer


class TimeDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a time."""

    queryset = fmt.Time.objects.all()
    serializer_class = serializers.TimeSerializer


class FormatList(generics.ListCreateAPIView):
    """List all formats, or create a new format."""

    queryset = fmt.Format.objects.all()
    serializer_class = serializers.FormatSerializer


class FormatDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a format."""

    queryset = fmt.Format.objects.all()
    serializer_class = serializers.FormatSerializer


class ClassificationList(generics.ListCreateAPIView):
    """List all classifications, or create a new classification."""

    queryset = fmt.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer


class ClassificationDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a classification."""

    queryset = fmt.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer


class AssociationList(generics.ListCreateAPIView):
    """List all associations, or create a new association."""

    queryset = fmt.Association.objects.all()
    serializer_class = serializers.AssociationSerializer


class AssociationDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an association."""

    queryset = fmt.Association.objects.all()
    serializer_class = serializers.AssociationSerializer
