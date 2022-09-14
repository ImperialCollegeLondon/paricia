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
    """
    List all countries, or create a new country.
    """

    queryset = stn.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a country.
    """

    queryset = stn.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class RegionList(generics.ListCreateAPIView):
    """
    List all regions, or create a new region.
    """

    queryset = stn.Region.objects.all()
    serializer_class = serializers.RegionSerializer


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a region.
    """

    queryset = stn.Region.objects.all()
    serializer_class = serializers.RegionSerializer


class EcosystemList(generics.ListCreateAPIView):
    """
    List all ecosystems, or create a new ecosystem.
    """

    queryset = stn.Ecosystem.objects.all()
    serializer_class = serializers.EcosystemSerializer


class EcosystemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an ecosystem.
    """

    queryset = stn.Ecosystem.objects.all()
    serializer_class = serializers.EcosystemSerializer


class InstitutionList(generics.ListCreateAPIView):
    """
    List all institutions, or create a new institution.
    """

    queryset = stn.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer


class InstitutionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an institution.
    """

    queryset = stn.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer


class StationTypeList(generics.ListCreateAPIView):
    """
    List all station types, or create a new station type.
    """

    queryset = stn.StationType.objects.all()
    serializer_class = serializers.StationTypeSerializer


class StationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a station type.
    """

    queryset = stn.StationType.objects.all()
    serializer_class = serializers.StationTypeSerializer


class PlaceList(generics.ListCreateAPIView):
    """
    List all places, or create a new place.
    """

    queryset = stn.Place.objects.all()
    serializer_class = serializers.PlaceSerializer


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a place.
    """

    queryset = stn.Place.objects.all()
    serializer_class = serializers.PlaceSerializer


class BasinList(generics.ListCreateAPIView):
    """
    List all basins, or create a new basin.
    """

    queryset = stn.Basin.objects.all()
    serializer_class = serializers.BasinSerializer


class BasinDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a basin.
    """

    queryset = stn.Basin.objects.all()
    serializer_class = serializers.BasinSerializer


class PlaceBasinList(generics.ListCreateAPIView):
    """
    List all place basins, or create a new place basin.
    """

    queryset = stn.PlaceBasin.objects.all()
    serializer_class = serializers.PlaceBasinSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.PlaceBasinListSerializer
        return self.serializer_class


class PlaceBasinDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a place basin.
    """

    queryset = stn.PlaceBasin.objects.all()
    serializer_class = serializers.PlaceBasinSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.PlaceBasinListSerializer
        return self.serializer_class


class StationList(generics.ListCreateAPIView):
    """
    List all stations, or create a new station.
    """

    queryset = stn.Station.objects.all()
    serializer_class = serializers.StationSerializer


class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a station.
    """

    queryset = stn.Station.objects.all()
    serializer_class = serializers.StationSerializer
