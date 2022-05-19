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

import mimetypes
import os
import urllib

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max, Min, Q, Value
from django.db.models.functions import Replace
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

import station.models as stn
from home.functions import modelo_a_tabla_html
from medicion.models import *
from station.functions import excel_station


# ####################################################################################
class CountryList(PermissionRequiredMixin, TemplateView):
    template_name = "station/country_list.html"
    permission_required = "station.view_country"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "id",
            "name",
        ]
        model = stn.Country.objects.values_list(*fields)
        context["countries"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class CountryCreate(PermissionRequiredMixin, CreateView):
    model = stn.Country
    permission_required = "station.add_country"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class CountryDetail(PermissionRequiredMixin, DetailView):
    model = stn.Country
    permission_required = "station.view_country"


class CountryUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Country
    permission_required = "station.change_country"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class CountryDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Country
    permission_required = "station.delete_country"
    success_url = reverse_lazy("station:country_index")


# ####################################################################################
class RegionList(PermissionRequiredMixin, TemplateView):
    template_name = "station/region_list.html"
    permission_required = "station.view_region"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["id", "name", "country_id__name"]
        model = stn.Region.objects.values_list(*fields)
        context["regions"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class RegionCreate(PermissionRequiredMixin, CreateView):
    model = stn.Region
    permission_required = "station.add_region"
    fields = ["name", "country"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class RegionDetail(PermissionRequiredMixin, DetailView):
    model = stn.Region
    permission_required = "station.view_region"


class RegionUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Region
    permission_required = "station.change_region"
    fields = ["name", "country"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class RegionDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Region
    permission_required = "station.delete_region"
    success_url = reverse_lazy("station:region_index")


# ####################################################################################
class EcosystemList(PermissionRequiredMixin, TemplateView):
    template_name = "station/ecosystem_list.html"
    permission_required = "station.view_ecosystem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "id",
            "name",
        ]
        model = stn.Ecosystem.objects.values_list(*fields)
        context["ecosystems"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class EcosystemCreate(PermissionRequiredMixin, CreateView):
    model = stn.Ecosystem
    permission_required = "station.add_ecosystem"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class EcosystemDetail(PermissionRequiredMixin, DetailView):
    model = stn.Ecosystem
    permission_required = "station.view_ecosystem"


class EcosystemUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Ecosystem
    permission_required = "station.change_ecosystem"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class EcosystemDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Ecosystem
    permission_required = "station.delete_ecosystem"
    success_url = reverse_lazy("station:ecosystem_index")


# ####################################################################################
class InstitutionList(PermissionRequiredMixin, TemplateView):
    template_name = "station/institution_list.html"
    permission_required = "station.view_institution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["id", "name"]
        model = stn.Institution.objects.values_list(*fields)
        context["institutions"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class InstitutionCreate(PermissionRequiredMixin, CreateView):
    model = stn.Institution
    permission_required = "station.add_institution"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class InstitutionDetail(PermissionRequiredMixin, DetailView):
    model = stn.Institution
    permission_required = "station.view_institution"


class InstitutionUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Institution
    permission_required = "station.change_institution"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class InstitutionDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Institution
    permission_required = "station.delete_institution"
    success_url = reverse_lazy("station:institution_index")


# ####################################################################################


class StationTypeList(PermissionRequiredMixin, TemplateView):
    template_name = "station/station_type_list.html"
    permission_required = "station.view_stationtype"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "id",
            "name",
        ]
        model = stn.StationType.objects.values_list(*fields)
        context["station_types"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class StationTypeCreate(PermissionRequiredMixin, CreateView):
    model = stn.StationType
    permission_required = "station.add_stationtype"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class StationTypeDetail(PermissionRequiredMixin, DetailView):
    model = stn.StationType
    permission_required = "station.view_stationtype"


class StationTypeUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.StationType
    permission_required = "station.change_stationtype"
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class StationTypeDelete(PermissionRequiredMixin, DeleteView):
    model = stn.StationType
    permission_required = "station.delete_stationtype"
    success_url = reverse_lazy("station:station_type_index")


# ####################################################################################


class StationList(PermissionRequiredMixin, TemplateView):
    template_name = "station/station_list.html"
    permission_required = "station.view_station"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "station_id",
            "station_code",
            "station_name",
            "stationtype_id__name",
            "country_id__name",
            "region_id__name",
            "placebasin_id__place__name",
            "placebasin_id__basin__name",
            "ecosystem_id__name",
            "institution_id__name",
            "station_state",
            "station_latitude",
            "station_longitude",
            "station_altitude",
            "station_file",
            "station_external",
            "influence_km",
        ]
        model = stn.Station.objects.values_list(*fields)
        context["stations"] = modelo_a_tabla_html(model, col_extra=True)
        context["station_types"] = stn.StationType.objects.all()
        return context


class StationCreate(PermissionRequiredMixin, CreateView):
    model = stn.Station
    permission_required = "station.add_station"
    fields = [
        "station_code",
        "station_name",
        "stationtype",
        "country",
        "region",
        "ecosystem",
        "institution",
        "placebasin",
        "station_state",
        "station_latitude",
        "station_longitude",
        "station_altitude",
        "station_file",
        "station_external",
        "influence_km",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class StationDetail(PermissionRequiredMixin, DetailView):
    model = stn.Station
    permission_required = "station.view_station"


class StationUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Station
    permission_required = "station.change_station"
    fields = [
        "station_code",
        "station_name",
        "stationtype",
        "country",
        "region",
        "ecosystem",
        "institution",
        "placebasin",
        "station_state",
        "station_latitude",
        "station_longitude",
        "station_altitude",
        "station_file",
        "station_external",
        "influence_km",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class StationDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Station
    permission_required = "station.delete_station"
    success_url = reverse_lazy("station:station_index")


@permission_required("station.view_station")
def StationExport(request):
    stations = stn.Station.objects.all()
    response = excel_station(stations)
    return response


# ####################################################################################


class PlaceList(PermissionRequiredMixin, TemplateView):
    template_name = "station/place_list.html"
    permission_required = "station.view_place"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            "id",
            "name",
        ]
        model = stn.Place.objects.values_list(*fields)
        context["places"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class PlaceCreate(PermissionRequiredMixin, CreateView):
    model = stn.Place
    permission_required = "station.add_place"
    fields = ["name", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class PlaceDetail(PermissionRequiredMixin, DetailView):
    model = stn.Place
    permission_required = "station.view_place"


class PlaceUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Place
    permission_required = "station.change_place"
    fields = ["name", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class PlaceDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Place
    permission_required = "station.delete_place"
    success_url = reverse_lazy("station:place_index")


# ####################################################################################


class BasinList(PermissionRequiredMixin, TemplateView):
    template_name = "station/basin_list.html"
    permission_required = "station.view_basin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _modelo = stn.Basin.objects.annotate(
            file_filename=Replace("file", Value(stn.BASIN_FILE_PATH), Value(""))
        )
        fields = ["id", "name", "file_filename"]
        model = _modelo.values_list(*fields)
        context["basins"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class BasinCreate(PermissionRequiredMixin, CreateView):
    model = stn.Basin
    permission_required = "station.add_basin"
    fields = ["name", "imagen", "file"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class BasinDetail(PermissionRequiredMixin, DetailView):
    model = stn.Basin
    permission_required = "station.view_basin"


class BasinUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.Basin
    permission_required = "station.change_basin"
    fields = ["name", "imagen", "file"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class BasinDelete(PermissionRequiredMixin, DeleteView):
    model = stn.Basin
    permission_required = "station.delete_basin"
    success_url = reverse_lazy("station:basin_index")


# ####################################################################################


class PlaceBasinList(PermissionRequiredMixin, TemplateView):
    template_name = "station/placebasin_list.html"
    permission_required = "station.view_placebasin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = ["id", "place_id__name", "basin_id__name"]
        model = stn.PlaceBasin.objects.values_list(*fields)
        context["place_basin"] = modelo_a_tabla_html(model, col_extra=True)
        return context


class PlaceBasinCreate(PermissionRequiredMixin, CreateView):
    model = stn.PlaceBasin
    permission_required = "station.add_placebasin"
    fields = ["place", "basin", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class PlaceBasinDetail(PermissionRequiredMixin, DetailView):
    model = stn.PlaceBasin
    permission_required = "station.view_placebasin"


class PlaceBasinUpdate(PermissionRequiredMixin, UpdateView):
    model = stn.PlaceBasin
    permission_required = "station.change_placebasin"
    fields = ["place", "basin", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class PlaceBasinDelete(PermissionRequiredMixin, DeleteView):
    model = stn.PlaceBasin
    permission_required = "station.delete_placebasin"
    success_url = reverse_lazy("station:placebasin_index")


#############################
@permission_required("station.view_station")
def station_query(request):
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


# Listar fechaS


def listar_anio(request, station, var):
    model = "Var" + str(var) + "Medicion"
    model = globals()[model]
    validados = model.objects.filter(station_id__exact=station).aggregate(
        Max("fecha"), Min("fecha")
    )
    if validados["fecha__max"] is not None:
        validados["fecha__max"] = validados["fecha__max"].year
        validados["fecha__min"] = validados["fecha__min"].year
        fechas = list(range(validados["fecha__min"], validados["fecha__max"] + 1))
    else:
        fechas = ["No existen datos"]
    return JsonResponse(fechas, safe=False)
