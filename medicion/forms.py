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
from .models import CurvaDescarga
from estacion.models import Estacion, Tipo
from variable.models import Variable

class CurvaDescargaForm(forms.ModelForm):
    class Meta:
        model = CurvaDescarga
        fields = ['estacion', 'fecha', 'funcion']

    def __init__(self, *args, **kwargs):
        super(CurvaDescargaForm, self).__init__(*args, **kwargs)
        self.fields['estacion'].queryset = Estacion.objects.filter(
            tipo=Tipo.objects.get(id=3)
        )
class ValidacionSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_codigo').filter(est_externa=False, tipo__in=(1,2,3)), empty_label="Estación")
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').exclude(var_id='10'), empty_label="Variable")
    inicio = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), input_formats=['%Y-%m-%d'], label="Fecha de Inicio", required=True)
    fin = forms.DateField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), input_formats=['%Y-%m-%d'], label="Fecha de Fin", required=True)
    limite_inferior = forms.IntegerField(required=False)
    limite_superior = forms.IntegerField(required=False)
    #revalidar = forms.BooleanField(label="Revalidar", help_text='Marcar si deseas borrar la última validacion')
    def __init__(self, *args, **kwargs):
        super(ValidacionSearchForm, self).__init__(*args, **kwargs)
        self.fields['estacion'].widget.attrs['placeholder'] = self.fields['estacion'].label