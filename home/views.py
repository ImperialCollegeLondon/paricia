################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import OPCIONES_CARGA, CargaInicialForm


class HomePageView(TemplateView):
    template_name = "home.html"


class CargaInicialView(PermissionRequiredMixin, FormView):
    permission_required = "home.carga_inicial"
    template_name = "home/carga_inicial.html"
    form_class = CargaInicialForm
    success_url = reverse_lazy("home:carga_inicial")

    def form_valid(self, form):
        tabla = form.cleaned_data["tabla"]
        tabla_descrip = ""
        for e in OPCIONES_CARGA:
            if e[0] == tabla:
                tabla_descrip = e[1]
        try:
            execute_from_command_line(
                ["manage.py", "loaddata", settings.BASE_DIR + "/home/data/" + tabla]
            )
        except:
            mensaje_err = "Ha ocurrido un error en la carga " + tabla_descrip
            return self.render_to_response(
                self.get_context_data(mensaje_err=mensaje_err)
            )
        mensaje_ok = "Carga exitosa " + tabla_descrip
        return self.render_to_response(self.get_context_data(mensaje_ok=mensaje_ok))
        # return super().form_valid(form)


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_field_errors = []
        form_non_field_errors = []
        if self.request.is_ajax():
            for field in form:
                if field.errors:
                    for error in field.errors:
                        fila = {"label_tag": field.label, "error": error}
                        form_field_errors.append(fila)

            for error in form.non_field_errors():
                fila = {"error": error}
                form_non_field_errors.append(fila)
            data_error = {
                "form_field_errors": form_field_errors,
                "form_non_field_errors": form_non_field_errors,
            }
            # return JsonResponse(form.errors, status=400)
            return JsonResponse(data_error, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                #'pk': self.object.pk,
                "mensaje": "Registro Guardado"
            }
            return JsonResponse(data)
        else:
            return response
