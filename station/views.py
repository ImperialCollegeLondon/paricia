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

import mimetypes
import os
import urllib

import utm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max, Min, Q, Value
from django.db.models.functions import Replace
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from home.functions import *
from medicion.models import *

from .functions import *
from .models import *


# ####################################################################################
class PaisList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/pais_list.html"
    permission_required = "estacion.view_pais"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "id",
            "nombre",
        ]
        modelo = Pais.objects.values_list(*campos)
        context["paises"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class PaisCreate(PermissionRequiredMixin, CreateView):
    model = Pais
    permission_required = "estacion.add_pais"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class PaisDetail(PermissionRequiredMixin, DetailView):
    model = Pais
    permission_required = "estacion.view_pais"


class PaisUpdate(PermissionRequiredMixin, UpdateView):
    model = Pais
    permission_required = "estacion.change_pais"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class PaisDelete(PermissionRequiredMixin, DeleteView):
    model = Pais
    permission_required = "estacion.delete_pais"
    success_url = reverse_lazy("estacion:pais_index")


# ####################################################################################
class RegionList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/region_list.html"
    permission_required = "estacion.view_region"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ["id", "nombre", "pais_id__nombre"]
        modelo = Region.objects.values_list(*campos)
        context["regiones"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class RegionCreate(PermissionRequiredMixin, CreateView):
    model = Region
    permission_required = "estacion.add_region"
    fields = ["nombre", "pais"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class RegionDetail(PermissionRequiredMixin, DetailView):
    model = Region
    permission_required = "estacion.view_region"


class RegionUpdate(PermissionRequiredMixin, UpdateView):
    model = Region
    permission_required = "estacion.change_region"
    fields = ["nombre", "pais"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class RegionDelete(PermissionRequiredMixin, DeleteView):
    model = Region
    permission_required = "estacion.delete_region"
    success_url = reverse_lazy("estacion:region_index")


# ####################################################################################
class EcosistemaList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/ecosistema_list.html"
    permission_required = "estacion.view_ecosistema"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "id",
            "nombre",
        ]
        modelo = Ecosistema.objects.values_list(*campos)
        context["ecosistemas"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class EcosistemaCreate(PermissionRequiredMixin, CreateView):
    model = Ecosistema
    permission_required = "estacion.add_ecosistema"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class EcosistemaDetail(PermissionRequiredMixin, DetailView):
    model = Ecosistema
    permission_required = "estacion.view_ecosistema"


class EcosistemaUpdate(PermissionRequiredMixin, UpdateView):
    model = Ecosistema
    permission_required = "estacion.change_ecosistema"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class EcosistemaDelete(PermissionRequiredMixin, DeleteView):
    model = Ecosistema
    permission_required = "estacion.delete_ecosistema"
    success_url = reverse_lazy("estacion:ecosistema_index")


# ####################################################################################
class SocioList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/socio_list.html"
    permission_required = "estacion.view_socio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ["id", "nombre"]
        modelo = Socio.objects.values_list(*campos)
        context["socios"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SocioCreate(PermissionRequiredMixin, CreateView):
    model = Socio
    permission_required = "estacion.add_socio"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class SocioDetail(PermissionRequiredMixin, DetailView):
    model = Socio
    permission_required = "estacion.view_socio"


class SocioUpdate(PermissionRequiredMixin, UpdateView):
    model = Socio
    permission_required = "estacion.change_socio"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class SocioDelete(PermissionRequiredMixin, DeleteView):
    model = Socio
    permission_required = "estacion.delete_socio"
    success_url = reverse_lazy("estacion:socio_index")


# ####################################################################################


class TipoList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/tipo_list.html"
    permission_required = "estacion.view_tipo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "id",
            "nombre",
        ]
        modelo = Tipo.objects.values_list(*campos)
        context["tipos"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class TipoCreate(PermissionRequiredMixin, CreateView):
    model = Tipo
    permission_required = "estacion.add_tipo"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class TipoDetail(PermissionRequiredMixin, DetailView):
    model = Tipo
    permission_required = "estacion.view_tipo"


class TipoUpdate(PermissionRequiredMixin, UpdateView):
    model = Tipo
    permission_required = "estacion.change_tipo"
    fields = ["nombre"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class TipoDelete(PermissionRequiredMixin, DeleteView):
    model = Tipo
    permission_required = "estacion.delete_tipo"
    success_url = reverse_lazy("estacion:tipo_index")


# ####################################################################################


class EstacionList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/estacion_list.html"
    permission_required = "estacion.view_estacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "est_id",
            "est_codigo",
            "est_nombre",
            "tipo_id__nombre",
            "pais_id__nombre",
            "region_id__nombre",
            "sitiocuenca_id__sitio__nombre",
            "sitiocuenca_id__cuenca__nombre",
            "ecosistema_id__nombre",
            "socio_id__nombre",
            "est_estado",
            "est_latitud",
            "est_longitud",
            "est_altura",
            "est_ficha",
            "est_externa",
            "influencia_km",
        ]
        modelo = Estacion.objects.values_list(*campos)
        context["estaciones"] = modelo_a_tabla_html(modelo, col_extra=True)
        context["tipos_estacion"] = Tipo.objects.all()
        return context


class EstacionCreate(PermissionRequiredMixin, CreateView):
    model = Estacion
    permission_required = "estacion.add_estacion"
    fields = [
        "est_codigo",
        "est_nombre",
        "tipo",
        "pais",
        "region",
        "ecosistema",
        "socio",
        "sitiocuenca",
        "est_estado",
        "est_latitud",
        "est_longitud",
        "est_altura",
        "est_ficha",
        "est_externa",
        "influencia_km",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class EstacionDetail(PermissionRequiredMixin, DetailView):
    model = Estacion
    permission_required = "estacion.view_estacion"


class EstacionUpdate(PermissionRequiredMixin, UpdateView):
    model = Estacion
    permission_required = "estacion.change_estacion"
    fields = [
        "est_codigo",
        "est_nombre",
        "tipo",
        "pais",
        "region",
        "ecosistema",
        "socio",
        "sitiocuenca",
        "est_estado",
        "est_latitud",
        "est_longitud",
        "est_altura",
        "est_ficha",
        "est_externa",
        "influencia_km",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class EstacionDelete(PermissionRequiredMixin, DeleteView):
    model = Estacion
    permission_required = "estacion.delete_estacion"
    success_url = reverse_lazy("estacion:estacion_index")


@permission_required("estacion.view_estacion")
def EstacionExport(request):
    estaciones = Estacion.objects.all()
    response = excel_estacion(estaciones)
    return response


# ####################################################################################


class SitioList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/sitio_list.html"
    permission_required = "estacion.view_sitio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = [
            "id",
            "nombre",
        ]
        modelo = Sitio.objects.values_list(*campos)
        context["sitios"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SitioCreate(PermissionRequiredMixin, CreateView):
    model = Sitio
    permission_required = "estacion.add_sitio"
    fields = ["nombre", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class SitioDetail(PermissionRequiredMixin, DetailView):
    model = Sitio
    permission_required = "estacion.view_sitio"


class SitioUpdate(PermissionRequiredMixin, UpdateView):
    model = Sitio
    permission_required = "estacion.change_sitio"
    fields = ["nombre", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class SitioDelete(PermissionRequiredMixin, DeleteView):
    model = Sitio
    permission_required = "estacion.delete_sitio"
    success_url = reverse_lazy("estacion:sitio_index")


# ####################################################################################


class CuencaList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/cuenca_list.html"
    permission_required = "estacion.view_cuenca"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _modelo = Cuenca.objects.annotate(
            ficha_filename=Replace("ficha", Value(CUENCA_FICHA_PATH), Value(""))
        )
        campos = ["id", "nombre", "ficha_filename"]
        modelo = _modelo.values_list(*campos)
        context["cuencas"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class CuencaCreate(PermissionRequiredMixin, CreateView):
    model = Cuenca
    permission_required = "estacion.add_cuenca"
    fields = ["nombre", "imagen", "ficha"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class CuencaDetail(PermissionRequiredMixin, DetailView):
    model = Cuenca
    permission_required = "estacion.view_cuenca"


class CuencaUpdate(PermissionRequiredMixin, UpdateView):
    model = Cuenca
    permission_required = "estacion.change_cuenca"
    fields = ["nombre", "imagen", "ficha"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class CuencaDelete(PermissionRequiredMixin, DeleteView):
    model = Cuenca
    permission_required = "estacion.delete_cuenca"
    success_url = reverse_lazy("estacion:cuenca_index")


# ####################################################################################


class SitioCuencaList(PermissionRequiredMixin, TemplateView):
    template_name = "estacion/sitiocuenca_list.html"
    permission_required = "estacion.view_sitiocuenca"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ["id", "sitio_id__nombre", "cuenca_id__nombre"]
        modelo = SitioCuenca.objects.values_list(*campos)
        context["sitio_cuenca"] = modelo_a_tabla_html(modelo, col_extra=True)
        return context


class SitioCuencaCreate(PermissionRequiredMixin, CreateView):
    model = SitioCuenca
    permission_required = "estacion.add_sitiocuenca"
    fields = ["sitio", "cuenca", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class SitioCuencaDetail(PermissionRequiredMixin, DetailView):
    model = SitioCuenca
    permission_required = "estacion.view_sitiocuenca"


class SitioCuencaUpdate(PermissionRequiredMixin, UpdateView):
    model = SitioCuenca
    permission_required = "estacion.change_sitiocuenca"
    fields = ["sitio", "cuenca", "imagen"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class SitioCuencaDelete(PermissionRequiredMixin, DeleteView):
    model = SitioCuenca
    permission_required = "estacion.delete_sitiocuenca"
    success_url = reverse_lazy("estacion:sitiocuenca_index")


#############################
@permission_required("estacion.view_estacion")
def estacion_consulta(request):
    variable_id = sitio_id = cuenca_id = estacion_tipo_id = None
    filtro = Q()

    try:
        variable_id = int(request.GET.get("variable_id", None))
    except Exception as e:
        pass

    try:
        sitio_id = int(request.GET.get("sitio_id", None))
    except Exception as e:
        pass

    try:
        cuenca_id = int(request.GET.get("cuenca_id", None))
    except Exception as e:
        pass

    try:
        estacion_tipo_id = int(request.GET.get("estacion_tipo_id", None))
    except Exception as e:
        pass

    if variable_id:
        filtro &= Q(cruce__var_id_id=variable_id)
    if sitio_id:
        filtro &= Q(sitiocuenca__sitio_id=sitio_id)
    if cuenca_id:
        filtro &= Q(sitiocuenca__cuenca_id=cuenca_id)
    if estacion_tipo_id:
        filtro &= Q(tipo_id=estacion_tipo_id)

    estaciones = Estacion.objects.filter(filtro)

    imagen = None
    if cuenca_id:
        imagen = Cuenca.objects.get(id=cuenca_id).imagen
    elif sitio_id:
        imagen = Sitio.objects.get(id=sitio_id).imagen

    try:
        imagen_url = imagen.url
    except:
        imagen_url = ""

    lista = {"estaciones": {}, "imagen": imagen_url}

    for row in estaciones:
        # print(row.est_longitud)
        # print(row.est_altura)
        lista["estaciones"][row.est_id] = row.est_codigo
    return JsonResponse(lista)


# estaciones FONAG  en formato JSON
def datos_json_estaciones(request):
    import decimal

    if request.user.is_authenticated:
        estaciones = list(Estacion.objects.order_by("est_id").all())
    else:
        estaciones = list(Estacion.objects.order_by("est_id").filter(est_externa=False))

    features = []
    for item in estaciones:
        if (type(item.est_latitud) is not type(None)) and (
            type(item.est_longitud) is not type(None)
        ):
            # if  item.est_latitud > 100 and item.est_latitud < 10000000 and item.est_longitud < 10000000 :
            #     lon_col = utm.to_latlon(float(item.est_longitud), float(item.est_latitud), 17.41666, 'M')
            #     item.est_longitud= lon_col[1]
            #     item.est_latitud= lon_col[0]
            # else:
            #     item.est_longitud= 0
            #     item.est_latitud= 0
            fila = dict(
                type="Feature",
                geometry=dict(
                    type="Point",
                    coordinates=[float(item.est_longitud), float(item.est_latitud)],
                ),
                properties=dict(
                    codigo=item.est_codigo,
                    nombre=item.est_nombre,
                    tipo=item.tipo.nombre,
                    latitud=item.est_latitud,
                    longitud=item.est_longitud,
                    altura=item.est_altura,
                ),
            )
            features.append(fila)
    datos = dict(type="FeatureCollection", features=features)
    return JsonResponse(datos, safe=False)


# Listar fechaS


def listar_anio(request, estacion, var):
    modelo = "Var" + str(var) + "Medicion"
    modelo = globals()[modelo]
    validados = modelo.objects.filter(estacion_id__exact=estacion).aggregate(
        Max("fecha"), Min("fecha")
    )
    if validados["fecha__max"] != None:
        validados["fecha__max"] = validados["fecha__max"].year
        validados["fecha__min"] = validados["fecha__min"].year
        fechas = list(range(validados["fecha__min"], validados["fecha__max"] + 1))
    else:
        fechas = ["No existen datos"]
    return JsonResponse(fechas, safe=False)


@permission_required("estacion.view_cuenca")
def cuenca_download_ficha(request, pk):
    cuenca = Cuenca.objects.get(pk=pk)
    file_path = cuenca.ficha.path
    output_filename = os.path.basename(file_path)
    fp = open(file_path, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(output_filename)
    if type is None:
        type = "application/octet-stream"
    response["Content-Type"] = type
    response["Content-Length"] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response["Content-Encoding"] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if "WebKit" in request.META["HTTP_USER_AGENT"]:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        # filename_header = 'filename=%s' % output_filename.encode('utf-8')
        filename_header = "filename=%s" % urllib.parse.quote(
            output_filename.encode("utf-8")
        )
    elif "MSIE" in request.META["HTTP_USER_AGENT"]:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ""
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        # filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(output_filename.encode('utf-8'))
        filename_header = "filename*=UTF-8''%s" % urllib.parse.quote(
            output_filename.encode("utf-8")
        )
    response["Content-Disposition"] = "attachment; " + filename_header
    return response
