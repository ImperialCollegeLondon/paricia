# -*- coding: utf-8 -*-

from django import forms
from instalacion.models import Instalacion
from estacion.models import Estacion
from datalogger.models import Datalogger


class InstalacionSearchForm(forms.Form):
    dat_id = forms.ModelChoiceField(label="Datalogger", required=False,
                                    queryset=Datalogger.objects.all())
    est_id = forms.ModelChoiceField(label="Estación", required=False,
                                    queryset=Datalogger.objects.all())

    def filtrar(self, form):
        dat_id = form.cleaned_data['dat_id']
        est_id = form.cleaned_data['est_id']
        if dat_id and est_id:
            lista = Instalacion.objects.filter(
                dat_id=dat_id
            ).filter(
                est_id=est_id
            )
        elif dat_id is None and est_id:
            lista = Instalacion.objects.filter(
                est_id=est_id
            )
        elif est_id is None and dat_id:
            lista = Instalacion.objects.filter(
                dat_id=dat_id
            )
        else:
            lista = Instalacion.objects.all()
        return lista
