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
from variable.models import Variable, Unidad
from cruce.models import Cruce
from django.contrib.auth.models import AnonymousUser

FILTRO = (
    ('todas_estaciones', 'Todas las estaciones'),
    ('sitio_cuenca', 'Sitio y Cuenca'),
)

FILTRO2 = (
    ('todas_estaciones', 'Todas las estaciones'),
    ('sitio_cuenca', 'Por Sitio'),
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


# Formulario para consultar los datos validados por periodo
class ConsultasPeriodoForm(forms.Form):
    lista_frecuencias = (
        ('0', 'Minima'),
        ('1', 'Horario'),
        ('2', 'Diario'),
        ('3', 'Mensual'),
    )
    lista_transmision = (
        ('0', 'Todo'),
        ('1', 'Automática'),
        ('2', 'Manual'),
    )
    transmision = forms.ChoiceField(choices=lista_transmision)
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.filter(est_externa=False).order_by('est_codigo'))
    variable = forms.ModelChoiceField(
    #    queryset=Variable.objects.order_by('var_id').filter(modulos='Hidroclimatico'))
            queryset=Variable.objects.order_by('var_id'))
    # inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)",required=False)
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)

    def __init__(self, *args, **kwargs):
        # super(MedicionSearchForm, self).__init__(*args, **kwargs)
        is_authenticated = kwargs.pop('is_authenticated', None)
        super(ConsultasPeriodoForm, self).__init__(*args, **kwargs)

        if is_authenticated:
            print("logueado")
            self.fields['estacion'] = forms.ModelChoiceField(
                queryset=Estacion.objects.all().order_by('est_codigo'))
        else:
            print("invitado")
            self.fields['estacion'] = forms.ModelChoiceField(
                queryset=Estacion.objects.filter(est_externa=False).order_by('est_codigo'))




class UsuarioSearchForm(forms.Form):
    lista_frecuencias = (
        ('0', 'Minima'),
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
        queryset=Estacion.objects.filter(est_externa=False).order_by('est_codigo'))
    variable = forms.ModelChoiceField(
        #queryset=Variable.objects.order_by('var_id').filter(modulos='Hidroclimatico'))
        queryset=Variable.objects.order_by('var_id'))

    # inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio(dd/mm/yyyy)",required=False)
    inicio = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Inicio", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    fin = forms.DateField(input_formats=['%d/%m/%Y'], label="Fecha de Fin", required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder':'dd/mm/yy'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)


# Formulario para las consultas de Sitio Cuenca
class ConsultasForm(forms.Form):
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS_TOTAL, label="Frecuencia")
    filtro = forms.ChoiceField(choices=FILTRO, widget=forms.RadioSelect(), initial=FILTRO[0][0], label="Filtro")
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.all(), label="Estacion", required=False)
    sitio = forms.ModelChoiceField(queryset=Sitio.objects.order_by('id').all(), label="Sitio", required=False)
    cuenca = forms.ModelChoiceField(queryset=Cuenca.objects.order_by('id').all(), label="Cuenca", required=False)
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


# Formulario para comparar varias estaciones por una sola variable
class ComparacionForm(forms.Form):
    estacion = forms.MultipleChoiceField(
        # choices=Estacion.objects.order_by().values('est_codigo').all(),
        choices=[],
        label="Estación", widget=forms.CheckboxSelectMultiple)
    lista_frecuencias = (
        # ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )

    #variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').filter(modulos='Hidroclimatico'),
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id'),
                                      label='Variable', initial=1)
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Inicio", widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'yyyy-mm-dd'}))
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin", widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'yyyy-mm-dd'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)

    def __init__(self, *args, **kwargs):
        super(ComparacionForm, self).__init__(*args, **kwargs)
        estaciones = Cruce.objects.filter(var_id=1).order_by('est_id').distinct()
        lista = []
        for e in estaciones:
            lista.append([e.est_id.est_id, e.est_id.est_codigo])
        self.fields['estacion'].choices = lista


# Formulario de Visitantes para comparar varias estaciones por una sola variable
class ComparacionFormPublico(forms.Form):
    estacion = forms.MultipleChoiceField(
        choices=[],
        label="Estación", widget=forms.CheckboxSelectMultiple)
    lista_frecuencias = (
        # ('1', '5 Minutos'),
        ('2', 'Horario'),
        ('3', 'Diario'),
        ('4', 'Mensual'),
    )

    #variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id').filter(modulos='Hidroclimatico'),
    variable = forms.ModelChoiceField(queryset=Variable.objects.order_by('var_id'),
                                      label='Variable', initial=1)
    inicio = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Inicio", widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'yyyy-mm-dd'}))
    fin = forms.DateField(input_formats=['%Y-%m-%d'], label="Fecha de Fin", widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'placeholder': 'yyyy-mm-dd'}))
    frecuencia = forms.ChoiceField(choices=lista_frecuencias)

    def __init__(self, *args, **kwargs):
        super(ComparacionFormPublico, self).__init__(*args, **kwargs)
        estaciones = Cruce.objects.filter(var_id=1, est_id__est_externa=False).order_by('est_id').distinct()
        lista = []
        for e in estaciones:
            lista.append([e.est_id.est_id, e.est_id.est_codigo])
        self.fields['estacion'].choices = lista


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
    #est_con01 = Estacion.objects.order_by('est_id').filter(tipo__tip_nombre="Hidrológica")
    est_con01 = Estacion.objects.order_by('est_id')
    lbl_est01 = 'Estación Hidrológica'
    #est_con02 = Estacion.objects.order_by('est_id').exclude(tipo__tip_nombre="Hidrológica")
    est_con02 = Estacion.objects.order_by('est_id')
    lbl_est02 = 'Estación Climática'
    var_con01 = Variable.objects.order_by('var_id').filter(var_id__in=[10, 11])
    var_con02 = Variable.objects.order_by('var_id').filter(var_id=1)
    parametros_widget = forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'})
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


class VariableFormPublico(forms.Form):
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
    #est_con01 = Estacion.objects.order_by('est_id').filter(tipo__tip_nombre="Hidrológica", est_externa=False)
    est_con01 = Estacion.objects.order_by('est_id')
    lbl_est01 = 'Estación Hidrológica'
    #est_con02 = Estacion.objects.order_by('est_id').exclude(tipo__tip_nombre="Hidrológica").filter(est_externa=False)
    est_con02 = Estacion.objects.order_by('est_id')
    lbl_est02 = 'Estación Climática'
    var_con01 = Variable.objects.order_by('var_id').filter(var_id__in=[10, 11])
    var_con02 = Variable.objects.order_by('var_id').filter(var_id=1)
    parametros_widget = forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'dd/mm/yy'})
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
