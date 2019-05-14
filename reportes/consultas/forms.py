# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion
from variable.models import Variable, Unidad


class MedicionSearchForm(forms.Form):
    lista_frecuencias = (
        ('0', 'Minima'),
        #('1', '5 Minutos'),
        ('1', 'Horario'),
        ('2', 'Diario'),
        ('3', 'Mensual'),
    )
    lista_transmision = (
        ('0','Todo'),
        ('1', 'Automática'),
        ('2', 'Manual'),
    )
    transmision = forms.ChoiceField(choices=lista_transmision)
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())

    # inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)",required=False)
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)


class UsuarioSearchForm(forms.Form):
    lista_frecuencias = (

        ('1', 'Horario'),
        ('2', 'Diario'),
        ('3', 'Mensual'),
    )
    lista_transmision = (
        ('0', 'Todo'),
        ('1', 'Automática'),
        ('1', 'Manual'),
    )
    transmision = forms.ChoiceField(choices=lista_transmision)
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())

    # inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)",required=False)
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)


class ComparacionForm(forms.Form):
    lista_frecuencias = (
        # ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )
    estacion01 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label='Primera Estación')
    estacion02 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label='Segunda Estación')
    estacion03 = forms.ModelChoiceField(queryset=Estacion.objects.order_by('est_id').all(), label='Tercera Estación')
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').all(), label='Variable')
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)


class VariableForm(forms.Form):
    lista_frecuencias = (
        # ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )
    lista_tipos = (
        # ('1', '5 Minutos'),
        ('1', 'Promedio'),
        ('2', 'Máximo'),
        ('3', 'Mínimo'),
    )
    est_con01 = Estacion.objects.order_by('est_id').filter(tipo__tip_nombre="Hidrológica")
    lbl_est01 = 'Estación Hidrológica'
    est_con02 = Estacion.objects.order_by('est_id').exclude(tipo__tip_nombre="Hidrológica")
    lbl_est02 = 'Estación Climática'
    var_con01 = Variable.objects.order_by('var_id').filter(var_id__in=[10, 11])
    var_con02 = Variable.objects.order_by('var_id').filter(var_id=1)
    parametros_widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'})
    format_input = ['%d/%m/%Y']
    lbl_inicio = 'Fecha de Inicio'
    lbl_fin = 'Fecha de Fin'
    estacion01 = forms.ModelChoiceField(queryset=est_con01, label=lbl_est01)
    variable01 = forms.ModelChoiceField(queryset=var_con01, label='Variable Hidrológica')
    parametro = forms.ChoiceField(choices=lista_tipos, label="Parámetro")
    estacion02 = forms.ModelChoiceField(queryset=est_con02, label=lbl_est02)
    variable02 = forms.ModelChoiceField(queryset=var_con02, label='Variable Climática')
    inicio = forms.DateField(input_formats=format_input, label=lbl_inicio, widget=parametros_widget)
    fin = forms.DateField(input_formats=format_input, label=lbl_fin, widget=parametros_widget)
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)


class EstacionVariableSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.order_by('est_id').all())
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
