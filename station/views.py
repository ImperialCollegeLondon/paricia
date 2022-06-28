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

from __future__ import unicode_literals

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max, Min, Q, Value
from django.db.models.functions import Replace
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from rest_framework import generics

import station.models as stn
import station.serializers as serializers
from station.functions import excel_station
from utilities.functions import modelo_a_tabla_html


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


############################################################################


@permission_required("station.view_station")
def station_query(request):
    """
    Station query view to get the station based on various possible
    query terms.
    NOTE: Lots of bare except statements and it's unclear when/why this
          would be used. Do we need it?
    """
    variable_id = place_id = basin_id = station_type_id = None
    filter_query = Q()

    try:
        variable_id = int(request.GET.get("variable_id", None))
    except Exception as e:
        pass

    try:
        place_id = int(request.GET.get("place_id", None))
    except Exception as e:
        pass

    try:
        basin_id = int(request.GET.get("basin_id", None))
    except Exception as e:
        pass

    try:
        station_type_id = int(request.GET.get("station_type_id", None))
    except Exception as e:
        pass

    # NOTE: cruce has been (for now at least) removed so this query is broken
    if variable_id:
        filter_query &= Q(cruce__var_id_id=variable_id)
    if place_id:
        filter_query &= Q(placebasin__place_id=place_id)
    if basin_id:
        filter_query &= Q(placebasin__basin_id=basin_id)
    if station_type_id:
        filter_query &= Q(station_type_id=station_type_id)

    stations = stn.Station.objects.filter(filter_query)

    imagen = None
    if basin_id:
        imagen = stn.Basin.objects.get(id=basin_id).imagen
    elif place_id:
        imagen = stn.Place.objects.get(id=place_id).imagen

    try:
        imagen_url = imagen.url
    except:
        imagen_url = ""

    lista = {"stations": {}, "imagen": imagen_url}

    for row in stations:
        # print(row.station_longitude)
        # print(row.station_altitude)
        lista["stations"][row.station_id] = row.station_code
    return JsonResponse(lista)


def list_year(request, station, var):
    """
    List data for a number of whole calendar years.
    """

    model = "Var" + str(var) + "Measurement"
    model = globals()[model]
    valid = model.objects.filter(station_id__exact=station).aggregate(
        Max("date"), Min("date")
    )
    if valid["date__max"] is not None:
        valid["date__max"] = valid["date__max"].year
        valid["date__min"] = valid["date__min"].year
        dates = list(range(valid["date__min"], valid["date__max"] + 1))
    else:
        dates = ["No data"]
    return JsonResponse(dates, safe=False)
