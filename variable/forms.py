# -*- coding: utf-8 -*-

from django import forms
from variable.models import Control
from estacion.models import Estacion
from formato.models import Variable


# from sensor.models import Sensor

class ControlSearchForm(forms.Form):
    var_id = forms.ModelChoiceField(label="Variable", required=False,
                                    queryset=Variable.objects.all())
    est_id = forms.ModelChoiceField(label="Estacion", required=False,
                                    queryset=Estacion.objects.all())

    def filtrar(self, form):
        var_id = form.cleaned_data['var_id']
        est_id = form.cleaned_data['est_id']
        if var_id and est_id:
            lista = Control.objects.filter(
                var_id=var_id
            ).filter(
                est_id=est_id
            )
        elif var_id is None and est_id:
            lista = Control.objects.filter(
                est_id=est_id
            )
        elif est_id is None and var_id:
            lista = Control.objects.filter(
                var_id=var_id
            )
        else:
            lista = Control.objects.all()
        return lista
