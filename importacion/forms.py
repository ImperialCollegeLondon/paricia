# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from importacion.models import Importacion


class ImportacionForm(forms.Form):
    imp_observacion = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': '3'}),
                                      initial="Carga de Datos")


class ImportacionSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(required=False,
                                      queryset=Estacion.objects.order_by('est_id').all())
    fecha = forms.DateField(required=False, label="Fecha de Importación(dd/mm/yyyy)", input_formats=['%d/%m/%Y'])
    lista = []

    def filtrar(self, form):
        estacion = form.cleaned_data['estacion']
        fecha = form.cleaned_data['fecha']
        if estacion and fecha:
            lista = Importacion.objects.filter(est_id=estacion
                                               ).filter(imp_fecha__range=[fecha, fecha])
        elif estacion is None and fecha:
            lista = Importacion.objects.filter(imp_fecha__date=fecha)
        elif fecha == "" and estacion:
            lista = Importacion.objects.filter(est_id=estacion)
        else:
            lista = Importacion.objects.all()
        return lista
