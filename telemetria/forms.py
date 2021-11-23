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
from telemetria.models import ConfigVisualizar, TeleVariables
from estacion.models import Estacion
from .functions import primer_dia_mes_actual, dia_hoy
from django.db import connection
import datetime

class ConsultaForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.none(), label="Estacion", required=False)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fecha de inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(pk__in=ConfigVisualizar.objects.values('estacion_id')).distinct()
        self.fields['estacion'].queryset = estaciones
        self.fields['estacion'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo


class AlarmaTransmisionLimitesForm(forms.Form):
    lim_inf = forms.DecimalField(max_digits=4, decimal_places=1, required=True, label='Límite 1, EXPECTANTE')
    lim_sup = forms.DecimalField(max_digits=4, decimal_places=1, required=True, label='Límite 2, FALLO')

    def __init__(self, *args, **kwargs):
        super(AlarmaTransmisionLimitesForm, self).__init__(*args, **kwargs)
        self.fields['lim_inf'].initial = round(TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_INFE').valor, 1)
        self.fields['lim_sup'].initial = round(TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_SUPE').valor, 1)



class PrecipitacionForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.none(), label="Estacion", required=False)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        initial=primer_dia_mes_actual
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fin", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),

    )

    def __init__(self, *args, **kwargs):
        super(PrecipitacionForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(pk__in=ConfigVisualizar.objects.filter(variable_id=1).values('estacion_id'))
        self.fields['estacion'].queryset = estaciones
        self.fields['estacion'].label_from_instance = self.label_from_instance
        estacion1 = estaciones[:1].get()
        self.fields['estacion'].initial = estacion1.est_id

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo


class PrecipitacionMultiestacionForm(forms.Form):
    estacion = forms.MultipleChoiceField(choices=[], label="Estación", widget=forms.CheckboxSelectMultiple)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        initial=dia_hoy
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fin", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
        initial=dia_hoy
    )

    def __init__(self, *args, **kwargs):
        super(PrecipitacionMultiestacionForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(
            pk__in=ConfigVisualizar.objects.filter(variable_id=1).values('estacion_id')
        ).distinct()
        lista = []
        for e in estaciones:
            lista.append([e.est_id, e.est_codigo])
        self.fields['estacion'].choices = lista




