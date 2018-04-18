# -*- coding: utf-8 -*-
from django import forms
from datalogger.models import Datalogger
from marca.models import Marca


class DataloggerSearchForm(forms.Form):
    marca = forms.ModelChoiceField(required=False,
                                   queryset=Marca.objects.order_by('mar_id').all())
    modelo = forms.CharField(label="Modelo", required=False)

    def filtrar(self, form):
        mar_id = form.cleaned_data['marca']
        dat_modelo = form.cleaned_data['modelo']
        # filtra los resultados en base al form
        if mar_id and dat_modelo:
            lista = Datalogger.objects.filter(
                mar_id=mar_id
            ).filter(
                dat_modelo=dat_modelo
            )
        elif mar_id is None and dat_modelo:
            lista = Datalogger.objects.filter(
                dat_modelo__icontains=dat_modelo
            )
        elif dat_modelo == "" and mar_id:
            lista = Datalogger.objects.filter(
                mar_id=mar_id
            )
        else:
            lista = Datalogger.objects.all()
        return lista
