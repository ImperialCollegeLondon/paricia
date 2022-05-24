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
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from home.functions import modelo_a_tabla_html
from medicion.models import DischargeCurve, LevelFunction

from .forms import LevelFunctionForm
from .functions import level_function_table


class DischargeCurveList(PermissionRequiredMixin, TemplateView):
    template_name = "medicion/dischargecurve_list.html"
    permission_required = "medicion.view_dischargecurve"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campos = ["id", "station__station_code", "date", "require_recalculate_flow"]
        dischargecurve = DischargeCurve.objects.all().values_list(*campos)
        context["dischargecurve"] = modelo_a_tabla_html(dischargecurve, col_extra=True)
        return context


class DischargeCurveCreate(PermissionRequiredMixin, CreateView):
    model = DischargeCurve
    fields = ["station", "date"]
    permission_required = "medicion.add_dischargecurve"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create"
        return context


class DischargeCurveDetail(PermissionRequiredMixin, DetailView):
    model = DischargeCurve
    permission_required = "medicion.view_dischargecurve"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dischargecurve_id = self.object.pk
        context["levelfunctiontable"] = level_function_table(dischargecurve_id)
        return context


class DischargeCurveUpdate(PermissionRequiredMixin, UpdateView):
    model = DischargeCurve
    permission_required = "medicion.change_dischargecurve"
    fields = ["station", "date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        return context


class DischargeCurveDelete(PermissionRequiredMixin, DeleteView):
    model = DischargeCurve
    permission_required = "medicion.delete_dischargecurve"
    success_url = reverse_lazy("medicion:dischargecurve_index")


class LevelFunctionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "medicion.add_dischargecurve"
    model = LevelFunction
    form_class = LevelFunctionForm

    def post(self, request, *args, **kwargs):
        dischargecurve_id = kwargs.get("id")
        dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
        form = LevelFunctionForm(self.request.POST or None)
        try:
            # Verify if form is correct
            levelfunction = form.save(commit=False)
        except Exception:
            # If it is not, send an informative message.
            _levelfunctiontable = level_function_table(dischargecurve_id)
            new_levelfunction = render(
                request,
                "medicion/levelfunction_form.html",
                {"form": LevelFunctionForm(self.request.POST or None)},
            )
            return render(
                request,
                "medicion/dischargecurve_detail.html",
                {
                    "dischargecurve": dischargecurve,
                    "levelfunctiontable": _levelfunctiontable,
                    "new_levelfunction": new_levelfunction.content.decode("utf-8"),
                },
            )
        levelfunction.dischargecurve = dischargecurve
        levelfunction.save()
        dischargecurve.requiere_recalculo_caudal = True
        dischargecurve.save()
        url = reverse(
            "medicion:dischargecurve_detail", kwargs={"pk": dischargecurve_id}
        )
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(LevelFunctionCreate, self).get_context_data(**kwargs)
        context["title"] = "Create"
        dischargecurve_id = self.kwargs.get("id")
        context["url"] = reverse(
            "medicion:levelfunction_create", kwargs={"id": dischargecurve_id}
        )
        return context


class LevelFunctionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "medicion.change_dischargecurve"
    model = LevelFunction
    fields = ["level", "function"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modify"
        levelfunction_pk = self.kwargs.get("pk")
        context["url"] = reverse(
            "medicion:levelfunction_update", kwargs={"pk": levelfunction_pk}
        )
        context["dischargecurve_id"] = self.object.dischargecurve.id
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        dischargecurve_id = data.get("dischargecurve_id")
        dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
        dischargecurve.require_recalculate_flow = True
        dischargecurve.save()
        self.success_url = reverse(
            "medicion:dischargecurve_detail", kwargs={"pk": dischargecurve_id}
        )
        return super().post(data, **kwargs)


class LevelFunctionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "medicion.delete_dischargecurve"
    model = LevelFunction

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        dischargecurve = self.object.dischargecurve
        dischargecurve.require_recalculate_flow = True
        dischargecurve.save()
        self.object.delete()
        return HttpResponseRedirect(
            reverse("medicion:dischargecurve_detail", kwargs={"pk": dischargecurve.id})
        )


class LevelFunctionDetail(PermissionRequiredMixin, DetailView):
    permission_required = "medicion.view_dischargecurve"
    model = LevelFunction


@permission_required("medicion.add_dischargecurve")
def recalculate_flow(request):
    dischargecurve_id = int(request.POST.get("dischargecurve_id", None))
    sql = "SELECT calculate_flow(%s);"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, [dischargecurve_id])
            cursor.fetchone()
    except Exception:
        lista = {"res": False}
        return JsonResponse(lista)
    dischargecurve = DischargeCurve.objects.get(pk=dischargecurve_id)
    dischargecurve.require_recalculate_flow = False
    dischargecurve.save()
    lista = {"res": True}
    return JsonResponse(lista)
