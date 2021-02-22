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

from django import forms
from estacion.models import Estacion
from importacion.models import Importacion


class ImportacionForm(forms.Form):
    imp_observacion = forms.CharField(label="Observación", required=False, widget=forms.Textarea(attrs={'rows': '3'}))


# class ImportacionSearchForm(forms.Form):
#     estacion = forms.ModelChoiceField(required=False,
#                                       queryset=Estacion.objects.order_by('est_id').all())
#     fecha = forms.DateField(required=False, label="Fecha de Importación(dd/mm/yyyy)", input_formats=['%d/%m/%Y'])
#     lista = []
#
#     def filtrar(self, form):
#         estacion = form.cleaned_data['estacion']
#         fecha = form.cleaned_data['fecha']
#         if estacion and fecha:
#             lista = Importacion.objects.filter(est_id=estacion).filter(imp_fecha__date=fecha)
#         elif estacion is None and fecha:
#             lista = Importacion.objects.filter(imp_fecha__date=fecha)
#         elif fecha is None and estacion:
#             lista = Importacion.objects.filter(est_id=estacion)
#         else:
#             lista = Importacion.objects.all()
#         return lista
