# -*- coding: utf-8 -*-

from django.forms import ModelForm
from cruce.models import Cruce
from estacion.models import Estacion
from variable.models import Variable


class CruceSearchForm(ModelForm):
    class Meta:
        model = Cruce
        fields = ['est_id', 'var_id']

    def filtrar(self, form):
        var_id = form.cleaned_data['var_id']
        est_id = form.cleaned_data['est_id']
        if var_id and est_id:
            lista = Cruce.objects.filter(
                var_id=var_id
            ).filter(
                est_id=est_id
            )
        elif var_id is None and est_id:
            lista = Cruce.objects.filter(
                est_id=est_id
            )
        elif est_id is None and var_id:
            lista = Cruce.objects.filter(
                var_id=var_id
            )
        else:
            lista = Cruce.objects.all()
        return lista

    def cadena(self, form):
        keys = form.cleaned_data.keys()
        string = str("?")
        i = 1
        for item in keys:
            if i < len(keys):
                string += item + "=" + str(form.cleaned_data[item]) + "&"
            else:
                string += item + "=" + str(form.cleaned_data[item])
            i += 1
        return string
