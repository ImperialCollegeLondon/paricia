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
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import connection
from django.db.models import F, Prefetch, Value, Window
from django.db.models.functions import Concat, Lag
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from home.functions import *
from medicion.models import DischargeCurve, LevelFunction
from variable.models import Variable

from .forms import NivelFuncionForm
from .functions import *


class CurvaDescargaList(PermissionRequiredMixin, TemplateView):
    template_name = "medicion/curvadescarga_list.html"
    permission_required = "medicion.view_curvadescarga"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ["id", "station__station_code", "fecha", "requiere_recalculo_caudal"]
        curvadescarga = DischargeCurve.objects.all().values_list(*campos)
        context["curvadescarga"] = modelo_a_tabla_html(curvadescarga, col_extra=True)
        return context


class CurvaDescargaCreate(PermissionRequiredMixin, CreateView):
    model = DischargeCurve
    fields = ["station", "fecha"]
    permission_required = "medicion.add_curvadescarga"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear"
        return context


class CurvaDescargaDetail(PermissionRequiredMixin, DetailView):
    model = DischargeCurve
    permission_required = "medicion.view_curvadescarga"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curvadescarga_id = self.object.pk
        context["nivelfunciontabla"] = nivelfunciontabla(curvadescarga_id)
        return context


class CurvaDescargaUpdate(PermissionRequiredMixin, UpdateView):
    model = DischargeCurve
    permission_required = "medicion.change_curvadescarga"
    fields = ["station", "fecha"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        return context


class CurvaDescargaDelete(PermissionRequiredMixin, DeleteView):
    model = DischargeCurve
    permission_required = "medicion.delete_curvadescarga"
    success_url = reverse_lazy("medicion:curvadescarga_index")


class NivelFuncionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "medicion.add_curvadescarga"
    model = LevelFunction
    form_class = NivelFuncionForm

    def post(self, request, *args, **kwargs):
        curvadescarga_id = kwargs.get("id")
        curvadescarga = DischargeCurve.objects.get(pk=curvadescarga_id)
        form = NivelFuncionForm(self.request.POST or None)
        try:
            ## Verificar si el formulario está correcto
            nivelfuncion = form.save(commit=False)
        except:
            ## Si no está correcto se envía un mensaje de Error
            _nivelfunciontabla = nivelfunciontabla(curvadescarga_id)
            new_nivelfuncion = render(
                request,
                "medicion/nivelfuncion_form.html",
                {"form": NivelFuncionForm(self.request.POST or None)},
            )
            return render(
                request,
                "medicion/curvadescarga_detail.html",
                {
                    "curvadescarga": curvadescarga,
                    "nivelfunciontabla": _nivelfunciontabla,
                    "new_nivelfuncion": new_nivelfuncion.content.decode("utf-8"),
                },
            )
        nivelfuncion.curvadescarga = curvadescarga
        nivelfuncion.save()
        curvadescarga.requiere_recalculo_caudal = True
        curvadescarga.save()
        url = reverse("medicion:curvadescarga_detail", kwargs={"pk": curvadescarga_id})
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(NivelFuncionCreate, self).get_context_data(**kwargs)
        context["title"] = "Crear"
        curvadescarga_id = self.kwargs.get("id")
        context["url"] = reverse(
            "medicion:nivelfuncion_create", kwargs={"id": curvadescarga_id}
        )
        return context


class NivelFuncionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "medicion.change_curvadescarga"
    model = LevelFunction
    fields = ["nivel", "funcion"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modificar"
        nivelfuncion_pk = self.kwargs.get("pk")
        context["url"] = reverse(
            "medicion:nivelfuncion_update", kwargs={"pk": nivelfuncion_pk}
        )
        context["curvadescarga_id"] = self.object.curvadescarga.id
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        curvadescarga_id = data.get("curvadescarga_id")
        curvadescarga = DischargeCurve.objects.get(pk=curvadescarga_id)
        curvadescarga.requiere_recalculo_caudal = True
        curvadescarga.save()
        self.success_url = reverse(
            "medicion:curvadescarga_detail", kwargs={"pk": curvadescarga_id}
        )
        return super().post(data, **kwargs)


class NivelFuncionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "medicion.delete_curvadescarga"
    model = LevelFunction

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        curvadescarga = self.object.curvadescarga
        curvadescarga.requiere_recalculo_caudal = True
        curvadescarga.save()
        self.object.delete()
        return HttpResponseRedirect(
            reverse("medicion:curvadescarga_detail", kwargs={"pk": curvadescarga.id})
        )


class NivelFuncionDetail(PermissionRequiredMixin, DetailView):
    permission_required = "medicion.view_curvadescarga"
    model = LevelFunction


@permission_required("medicion.add_curvadescarga")
def recalcular_caudal(request):
    curvadescarga_id = int(request.POST.get("curvadescarga_id", None))
    sql = "SELECT calcular_caudal(%s);"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, [curvadescarga_id])
            res = cursor.fetchone()
    except:
        lista = {"res": False}
        return JsonResponse(lista)
    curvadescarga = DischargeCurve.objects.get(pk=curvadescarga_id)
    curvadescarga.requiere_recalculo_caudal = False
    curvadescarga.save()
    lista = {"res": True}
    return JsonResponse(lista)
