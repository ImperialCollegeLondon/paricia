# -*- coding: utf-8 -*-
from django import forms
from estacion.models import Estacion, Sistema, Cuenca
from variable.models import Variable, Unidad

FILTRO = (
    ('todas_estaciones', 'Todas las estaciones'),
    ('sistema_cuenca', 'Sistema y Subcuenca'),
)

FILTRO2 = (
    ('todas_estaciones', 'Todas las estaciones'),
    ('sistema_cuenca', 'Por Sistema'),
)

FRECUENCIAS_TOTAL = (
    ('subhorario-crudo', 'Sub-horario Crudo'),
    ('subhorario-validado', 'Sub-horario Validado'),
    ('horario', 'Horario'),
    ('diario', 'Diario'),
    ('mensual', 'Mensual'),
)

FRECUENCIAS_VALIDADAS = (
    ('subhorario-validado', 'Sub-horario'),
    ('horario', 'Horario'),
    ('diario', 'Diario'),
    ('mensual', 'Mensual'),
)


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
        queryset=Estacion.objects.order_by('est_id').filter(est_externa=False))
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by('var_id').all())

    # inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)",required=False)
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)


class ConsultasForm(forms.Form):
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS_TOTAL, label="Frecuencia")
    filtro = forms.ChoiceField(choices=FILTRO, widget=forms.RadioSelect(), initial=FILTRO[0][0], label="Filtro")
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.all(), label="Estacion", required=False)
    sistema = forms.ModelChoiceField(queryset=Sistema.objects.order_by('id').all(), label="Sistema", required=False)
    cuenca = forms.ModelChoiceField(queryset=Cuenca.objects.order_by('id').all(), label="Subcuenca", required=False)
    variables = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14]
    variable = forms.ModelChoiceField(queryset=Variable.objects.filter(pk__in=variables), label="Variable", initial=1)
    inicio = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label="Fecha de inicio",
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label="Fecha de fin",
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    mensaje = ""

    def __init__(self, *args, **kwargs):
        try:
            # consulta = args[0]
            # print(consulta)
            super(ConsultasForm, self).__init__(*args, **kwargs)
            return
        except:
            pass

        frecuencias = FRECUENCIAS_VALIDADAS
        try:
            user = kwargs.pop('user')
            if user.username == "admin" or user.username == "tecnico":
                frecuencias = FRECUENCIAS_TOTAL
        except:
            pass

        super(ConsultasForm, self).__init__(*args, **kwargs)
        self.fields['frecuencia'] = forms.ChoiceField(choices=frecuencias, label="Frecuencia", initial=frecuencias[0][0])




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
