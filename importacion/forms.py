# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from estacion.models import Estacion
from importacion.models import Importacion, ImportacionTemp


class ImportacionForm(forms.Form):
    imp_observacion = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': '3'}),
                                      initial="Carga de Datos", label="Observaciones/Anotaciones")


class ImportacionSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(required=False,
                                      queryset=Estacion.objects.order_by('est_id').all())
    fecha = forms.DateField(required=False, label="Fecha de Importación(dd/mm/yyyy)", input_formats=['%d/%m/%Y'])
    lista = []

    def filtrar(self, form,tipo):
        estacion = form.cleaned_data['estacion']
        fecha = form.cleaned_data['fecha']
        if estacion and fecha:
            lista = Importacion.objects.filter(est_id=estacion
                    ).filter(imp_fecha__date=fecha).filter(imp_tipo=tipo)
        elif estacion is None and fecha is not None:
            lista = Importacion.objects.filter(imp_fecha__date=fecha).filter(imp_tipo=tipo)
        elif fecha is None and estacion is not None:
            lista = Importacion.objects.filter(est_id=estacion).filter(imp_tipo=tipo)
        else:
            lista = Importacion.objects.filter(imp_tipo=tipo)
        return lista


class ImportacionCreateForm(ModelForm):
    class Meta:
        model = ImportacionTemp
        fields = ['est_id', 'for_id', 'imp_archivo']

    def __init__(self, *args, **kwargs):
        super(ImportacionCreateForm, self).__init__(*args, **kwargs)
        self.fields['est_id'].queryset = Estacion.objects.filter(est_externa=False).order_by('est_codigo')
