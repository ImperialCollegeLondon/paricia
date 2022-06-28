########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosystems Andinos
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

import station.models as stn
import station.serializers as serializers


class CountryList(generics.ListCreateAPIView):
    queryset = stn.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class RegionList(generics.ListCreateAPIView):
    queryset = stn.Region.objects.all()
    serializer_class = serializers.RegionSerializer


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Region.objects.all()
    serializer_class = serializers.RegionSerializer


class EcosystemList(generics.ListCreateAPIView):
    queryset = stn.Ecosystem.objects.all()
    serializer_class = serializers.EcosystemSerializer


class EcosystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Ecosystem.objects.all()
    serializer_class = serializers.EcosystemSerializer


class InstitutionList(generics.ListCreateAPIView):
    queryset = stn.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer


class InstitutionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer


class StationTypeList(generics.ListCreateAPIView):
    queryset = stn.StationType.objects.all()
    serializer_class = serializers.StationTypeSerializer


class StationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.StationType.objects.all()
    serializer_class = serializers.StationTypeSerializer


class PlaceList(generics.ListCreateAPIView):
    queryset = stn.Place.objects.all()
    serializer_class = serializers.PlaceSerializer


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Place.objects.all()
    serializer_class = serializers.PlaceSerializer


class BasinList(generics.ListCreateAPIView):
    queryset = stn.Basin.objects.all()
    serializer_class = serializers.BasinSerializer


class BasinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Basin.objects.all()
    serializer_class = serializers.BasinSerializer


class PlaceBasinList(generics.ListCreateAPIView):
    queryset = stn.PlaceBasin.objects.all()
    serializer_class = serializers.PlaceBasinSerializer


class PlaceBasinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.PlaceBasin.objects.all()
    serializer_class = serializers.PlaceBasinSerializer


class StationList(generics.ListCreateAPIView):
    queryset = stn.Station.objects.all()
    serializer_class = serializers.StationSerializer


class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = stn.Station.objects.all()
    serializer_class = serializers.StationSerializer
