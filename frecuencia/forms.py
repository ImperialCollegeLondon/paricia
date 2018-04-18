# -*- coding: utf-8 -*-

from django.forms import ModelForm
from frecuencia.models import Frecuencia
from estacion.models import Estacion
from formato.models import Variable


class FrecuenciaSearchForm(ModelForm):
    class Meta:
        model = Frecuencia
        fields = ['est_id', 'var_id']

    lista = []

    # Variable = forms.ChoiceField(required=False,choices=lista_variables())
    # Estacion = forms.ChoiceField(required=False,choices=lista_estaciones())

    def filtrar(self, form):
        var_id = form.cleaned_data['var_id']
        est_id = form.cleaned_data['est_id']
        if var_id and est_id:
            lista = Frecuencia.objects.filter(
                var_id=var_id
            ).filter(
                est_id=est_id
            )
        elif var_id is None and est_id:
            lista = Frecuencia.objects.filter(
                est_id=est_id
            )
        elif est_id is None and var_id:
            lista = Frecuencia.objects.filter(
                var_id=var_id
            )
        else:
            lista = Frecuencia.objects.all()
        return lista

    def cadena(self, form):
        keys = form.cleaned_data.keys()
        string = str("?")
        i = 1
        for item in keys:
            if i < len(keys):
                string += item + "=" + str(form.cleaned_data[item].encode('utf-8')) + "&"
            else:
                string += item + "=" + str(form.cleaned_data[item])
            i += 1
        return string
