# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.


from django import forms
from estacion.models import Estacion, Sitio, Cuenca
from variable.models import Variable
from frecuencia.models import UsuarioTipoFrecuencia, TipoFrecuencia
import datetime


FILTRO = (
    ('todas_estaciones', 'Todas las estaciones'),
    ('sitio_cuenca', 'Sitio y cuenca'),
)

FILTRO2 = (
    ('todas_estaciones', 'Todas las estaciones'),
    ('sitio_cuenca', 'Por Sitio'),
)

PROFUNDIDADES = (
    (50, '0.50 m'),
    (500, '5.00 m'),
    (1000, '10.00 m'),
)

var_hidro_consulta_periodo = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14]

var_diario = [
    1,  # precipitacion
    # 10, # caudal
]

var_mensualmultianual = [
    1,  # precipitacion
    # 10, # caudal
]

año_actual = datetime.datetime.now().year
años = []
for a in range(2000, año_actual + 1):
    años.append((a, a))


class AnuarioForm(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.all(), label='Estación')
    anio = forms.ChoiceField(required=False, choices=años, label='Año', initial=año_actual)

    def __init__(self, *args, **kwargs):
        super(AnuarioForm, self).__init__(*args, **kwargs)
        self.fields['estacion'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo + str(" - ") + obj.est_nombre


class DiarioForm(forms.Form):
    filtro = forms.ChoiceField(choices=FILTRO, widget=forms.RadioSelect(), initial=FILTRO[0][0], label="Filtro")
    estacion_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    sitio = forms.ModelChoiceField(queryset=Sitio.objects.order_by('id').all(), label="Sitio", required=False)
    cuenca = forms.ModelChoiceField(queryset=Cuenca.objects.order_by('id').all(), label="Cuenca", required=False)
    variable = forms.ModelChoiceField(queryset=Variable.objects.filter(pk__in=var_diario),
                                      label="Variable", initial=var_diario[0], required=True)
    año = forms.ChoiceField(choices=años, label='Año', initial=año_actual, required=True)


class MensualMultianualForm(forms.Form):
    filtro = forms.ChoiceField(choices=FILTRO, widget=forms.RadioSelect(), initial=FILTRO[0][0], label="Filtro")
    estacion_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    sitio = forms.ModelChoiceField(queryset=Sitio.objects.order_by('id').all(), label="Sitio", required=False)
    cuenca = forms.ModelChoiceField(queryset=Cuenca.objects.order_by('id').all(), label="Cuenca", required=False)
    variable = forms.ModelChoiceField(queryset=Variable.objects.filter(pk__in=var_mensualmultianual),
                                      label="Variable", initial=var_mensualmultianual[0], required=True)
    año_inicio = forms.ChoiceField(choices=años, label='Año inicio', initial=años[0], required=False)
    año_fin = forms.ChoiceField(choices=años, label='Año fin', initial=año_actual, required=False)


class ConsultasForm(forms.Form):
    frecuencia = forms.ModelChoiceField(queryset=TipoFrecuencia.objects.none(), label="Frecuencia", required=True)
    filtro = forms.ChoiceField(choices=FILTRO, widget=forms.RadioSelect(), initial=FILTRO[0][0], label="Filtro", required=False)
    estacion_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    sitio = forms.ModelChoiceField(queryset=Sitio.objects.order_by('id').all(), label="Sitio", required=False)
    cuenca = forms.ModelChoiceField(queryset=Cuenca.objects.none(), label="Cuenca", required=False)
    variable = forms.ModelChoiceField(queryset=Variable.objects.filter(pk__in=var_hidro_consulta_periodo),
                                      label="Variable", initial=1, required=True)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], 
        label="Fecha de inicio", 
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], 
        label="Fecha de fin", 
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def __init__(self, *args, **kwargs):
        if len(kwargs):
            user = kwargs.pop('user')
        elif len(args):
            user = args[1]['user']

        if user.username == 'admin':
            frecuencia_queryset = TipoFrecuencia.objects.all().order_by('id')
        else:
            try:
                uf = UsuarioTipoFrecuencia.objects.filter(usuario=user)
                frecuencia_queryset = TipoFrecuencia.objects.filter(pk__in=uf.values('tipofrecuencia_id')).order_by('id')
            except:
                ## Aquí vendría AnonymousUser
                frecuencia_queryset = TipoFrecuencia.objects.filter(pk__in=(2,3,4,5)).order_by('id')

        super().__init__(*args, **kwargs)
        self.fields['frecuencia'].queryset = frecuencia_queryset


class CalidadConsultasForm(forms.Form):
    frecuencia = forms.ModelChoiceField(queryset=TipoFrecuencia.objects.none(), label="Frecuencia", required=True)
    filtro = forms.ChoiceField(choices=FILTRO2, widget=forms.RadioSelect(), initial=FILTRO2[0][0], label="Filtro")
    estacion_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    sitio = forms.ModelChoiceField(queryset=Sitio.objects.order_by('id').all(), label="Sitio", required=False)
    var_ids = (101, 102, 103, 104, 105, 106, 107, 108)
    variable = forms.ModelChoiceField(queryset=Variable.objects.filter(pk__in=var_ids), label="Variable",
                                      required=True, initial=var_ids[0])
    profundidad = forms.ChoiceField(choices=PROFUNDIDADES)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], 
        label="Inicio (yyyy-mm-dd)",
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], 
        label="Fin (yyyy-mm-dd)",
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def __init__(self, *args, **kwargs):
        if len(kwargs):
            user = kwargs.pop('user')
        elif len(args):
            user = args[1]['user']

        if user.username == 'admin':
            frecuencia_queryset = TipoFrecuencia.objects.all().order_by('id')
        else:
            try:
                uf = UsuarioTipoFrecuencia.objects.filter(usuario=user)
                frecuencia_queryset = TipoFrecuencia.objects.filter(pk__in=uf.values('tipofrecuencia_id')).order_by('id')
            except:
                ## Aquí vendría AnonymousUser
                frecuencia_queryset = TipoFrecuencia.objects.filter(pk__in=(2,3,4,5)).order_by('id')

        super().__init__(*args, **kwargs)
        self.fields['frecuencia'].queryset = frecuencia_queryset



#############################################################################################################
#############################################################################################################
#############################################################################################################

FRECUENCIAX = (
    ##('1', '5 Minutos'),
    (None, '---------'),
    ('2', 'Horario'),
    ('3', 'Diario'),
    ('4', 'Mensual'),
)

class ComparacionForm(forms.Form):
    estacion01 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Primera Estación')
    estacion02 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Segunda Estación')
    estacion03 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Tercera Estación')
    variable = forms.ModelChoiceField(required=False,
                                      queryset=Variable.objects.order_by('var_id').all(), label='Variable')
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Inicio (yyyy/mm/dd)",
                             widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin (yyyy/mm/dd)",
                          widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAX)


class VariableForm(forms.Form):
    estacion01 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Primera Estación')
    variable01 = forms.ModelChoiceField(required=False,
                                        queryset=Variable.objects.order_by('var_id').all(), label='Primera Variable')
    estacion02 = forms.ModelChoiceField(required=False,
                                        queryset=Estacion.objects.order_by('est_id').all(), label='Segunda Estación')
    variable02 = forms.ModelChoiceField(required=False,
                                        queryset=Variable.objects.order_by('var_id').all(), label='Segunda Variable')
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Inicio (yyyy/mm/dd)",
                             widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin (yyyy/mm/dd)",
                          widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    frecuencia = forms.ChoiceField(choices=FRECUENCIAX)