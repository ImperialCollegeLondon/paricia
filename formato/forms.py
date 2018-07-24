# -*- coding: utf-8 -*-

from django.forms import ModelForm
from formato.models import Formato, Clasificacion, Asociacion
from django import forms


class FormatoSearchForm(forms.Form):
    lista = []
    TIPO_FORMATO = (
        ('', 'Todos'),
        ('automatico', 'automático'),
        ('convencional', 'convencional'),
        ('ftp', 'ftp'),
    )
    for_descripcion = forms.CharField(
        max_length=200,
        required=False,
        help_text='Puede usar una o varias palabras',
        label='Descripción'
    )
    for_tipo=forms.ChoiceField(required=False, choices=TIPO_FORMATO)

    def filtrar(self, form):
        if form.cleaned_data['for_descripcion'] and form.cleaned_data['for_tipo']:
            lista = Formato.objects.filter(
                for_descripcion=form.cleaned_data['for_descripcion']
            ).filter(
                for_tipo=form.cleaned_data['for_tipo']
            )
        elif form.cleaned_data['for_tipo'] == "" and form.cleaned_data['for_descripcion'] != "":
            lista = Formato.objects.filter(
                for_descripcion__icontains=form.cleaned_data['for_descripcion']
            )
        elif form.cleaned_data['for_descripcion'] == "" and form.cleaned_data['for_tipo'] != "":
            lista = Formato.objects.filter(
                for_tipo=form.cleaned_data['for_tipo']
            )
        else:
            lista = Formato.objects.all()
        return lista


class FormatoForm(ModelForm):
    class Meta:
        model = Formato
        fields = '__all__'


class ClasificacionSearchForm(ModelForm):
    lista = []

    class Meta:
        model = Clasificacion
        fields = ['var_id', 'for_id']

    def filtrar(self, form):
        for_id = form.cleaned_data['for_id']
        var_id = form.cleaned_data['var_id']
        if var_id and for_id:
            lista = Clasificacion.objects.filter(
                var_id=var_id
            ).filter(
                for_id=for_id
            )
        elif var_id is None and for_id:
            lista = Clasificacion.objects.filter(
                for_id=for_id
            )
        elif for_id is None and var_id:
            lista = Clasificacion.objects.filter(
                var_id=var_id
            )
        elif var_id is None and for_id is None:
            lista = Clasificacion.objects.all()

        return lista


class ClasificacionForm(ModelForm):
    class Meta:
        model = Clasificacion
        fields = ['var_id', 'cla_valor', 'cla_maximo', 'cla_minimo']


class AsociacionSearchForm(ModelForm):
    lista = []

    class Meta:
        model = Asociacion
        fields = ['est_id', 'for_id']

    def filtrar(self, form):
        for_id = form.cleaned_data['for_id']
        est_id = form.cleaned_data['est_id']
        if est_id and for_id:
            lista = Asociacion.objects.filter(
                est_id=est_id
            ).filter(
                for_id=for_id
            )
        elif est_id is None and for_id:
            lista = Asociacion.objects.filter(
                for_id=for_id
            )
        elif for_id is None and est_id:
            lista = Asociacion.objects.filter(
                est_id=est_id
            )
        elif est_id is None and for_id is None:
            lista = Asociacion.objects.all()
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
