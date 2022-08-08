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

from django import forms
from django.core.exceptions import ValidationError
from django.db import connection

from station.models import Station
from variable.models import Variable

from .models import LevelFunction


class LevelFunctionForm(forms.ModelForm):
    class Meta:
        model = LevelFunction
        fields = ["level", "function"]

    def clean_function(self):
        function = self.cleaned_data["function"]

        # Verifica si tiene letra H
        if "H" not in function:
            raise ValidationError("It must include parameter H (water level)")

        # Verifica si la función devuelve resultado
        test_func = function.replace("H", "10")
        sql = "SELECT eval_math('" + test_func + "');"
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                len = cursor.rowcount
                cursor.fetchall()
        except Exception as err:
            raise ValidationError(f"Formula syntax error. {err}")

        if len < 1:
            raise ValidationError("Formula syntax error. No rows found!")
        return function


class ValidationSearchForm(forms.Form):
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
    start = forms.DateField(
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        input_formats=["%Y-%m-%d"],
        label="Start date",
        required=True,
    )
    end = forms.DateField(
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        input_formats=["%Y-%m-%d"],
        label="End date",
        required=True,
    )
    lower_limit = forms.IntegerField(required=False)
    upper_limit = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(ValidationSearchForm, self).__init__(*args, **kwargs)
        self.fields["station"].widget.attrs["placeholder"] = self.fields[
            "station"
        ].label
