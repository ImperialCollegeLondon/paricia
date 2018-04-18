# -*- coding: utf-8 -*-

from django import forms
# from uploads.core.models import Document
from estacion.models import Estacion


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ('est_nombre', 'est_ficha',)


class EstacionSearchForm(forms.Form):
    TIPO_ESTACION = (
        ('', '----'),
        ('M', 'Meteorológica'),
        ('P', 'Pluviométrica'),
        ('H', 'Hidrológica'),
    )

    lista = []
    Tipo = forms.ChoiceField(required=False, choices=TIPO_ESTACION)
    Codigo = forms.CharField(required=False, max_length=10)

    def filtrar(self, form):
        if form.cleaned_data['Tipo'] and form.cleaned_data['Codigo']:
            lista = Estacion.objects.filter(
                est_tipo=form.cleaned_data['Tipo']
            ).filter(
                est_codigo=form.cleaned_data['Codigo']
            )
        elif form.cleaned_data['Tipo'] == "" and form.cleaned_data['Codigo'] != "":
            lista = Estacion.objects.filter(
                est_codigo__icontains=form.cleaned_data['Codigo']
            )
        elif form.cleaned_data['Codigo'] == "" and form.cleaned_data['Tipo'] != "":
            lista = Estacion.objects.filter(
                est_tipo=form.cleaned_data['Tipo']
            )
        else:
            lista = Estacion.objects.all()
        return lista

    def cadena(self, form):
        keys = form.cleaned_data.keys()
        string = str("?")
        i = 1
        for item in keys:
            if i < len(keys):
                string += item + "=" + str(form.cleaned_data[item].encode('utf-8')) + "&"
            else:
                string += item + "=" + str(form.cleaned_data[item].encode('utf-8'))
            i += 1
        return string
