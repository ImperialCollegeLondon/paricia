# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from vacios.functions import consultar_vacios

from .forms import VaciosSearchForm


class Vacios(PermissionRequiredMixin, FormView):
    permission_required = "vacios.view_vacios"
    template_name = "vacios/form.html"
    form_class = VaciosSearchForm
    success_url = reverse_lazy("vacios:vacios")

    def post(self, request, *args, **kwargs):
        form = VaciosSearchForm(self.request.POST or None)
        if form.is_valid():
            if self.request.is_ajax():
                variable = form.cleaned_data["variable"]
                estacion = form.cleaned_data["estacion"]
                lista = consultar_vacios(estacion.est_id, variable.var_id)
                return render(
                    request,
                    "vacios/tabla.html",
                    {
                        "lista": lista,
                    },
                )
