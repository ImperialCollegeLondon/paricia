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
from django.core.exceptions import ValidationError
from django.db import connection

from station.models import Station, StationType
from variable.models import Variable

from .models import NivelFuncion


class NivelFuncionForm(forms.ModelForm):
    class Meta:
        model = NivelFuncion
        fields = ["nivel", "funcion"]

    def clean_funcion(self):
        funcion = self.cleaned_data["funcion"]

        ## Verifica si tiene letra H
        if "H" not in funcion:
            raise ValidationError("Debe incluir el parámetro H (nivel de agua)")

        ## Verifica si la función devuelve resultado
        test_func = funcion.replace("H", "10")
        sql = "SELECT eval_math('" + test_func + "');"
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                len = cursor.rowcount
                res = cursor.fetchall()
        except:
            raise ValidationError("Error en la sintáxis de la fórmula")
        if len < 1:
            raise ValidationError("Error en la sintáxis de la fórmula")
        return funcion


class ValidacionSearchForm(forms.Form):
    station = forms.ModelChoiceField(
        queryset=Station.objects.order_by("station_code").filter(
            station_external=False, station_type__in=(1, 2, 3)
        ),
        empty_label="Station",
    )
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by("variable_id").exclude(variable_id="10"),
        empty_label="Variable",
    )
    inicio = forms.DateField(
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        input_formats=["%Y-%m-%d"],
        label="Fecha de Inicio",
        required=True,
    )
    fin = forms.DateField(
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        input_formats=["%Y-%m-%d"],
        label="Fecha de Fin",
        required=True,
    )
    limite_inferior = forms.IntegerField(required=False)
    limite_superior = forms.IntegerField(required=False)
    # revalidar = forms.BooleanField(label="Revalidar", help_text='Marcar si deseas borrar la última validacion')
    def __init__(self, *args, **kwargs):
        super(ValidacionSearchForm, self).__init__(*args, **kwargs)
        self.fields["station"].widget.attrs["placeholder"] = self.fields[
            "station"
        ].label
