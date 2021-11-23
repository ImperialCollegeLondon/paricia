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
# from django_select2 import forms as s2forms
from estacion.models import Estacion
from variable.models import Variable
from cruce.models import Cruce
from . import models
from frecuencia.models import UsuarioTipoFrecuencia, TipoFrecuencia
from django.contrib import admin
from django.contrib.auth.models import User

vars_calidad = (101, 102, 103, 104, 105, 106, 107, 108)
vars_hidro = (1, 2, 3, 4, 5, 7, 8, 11)

class Grafico1Form(forms.Form):
    estacion = forms.ModelChoiceField(queryset=Estacion.objects.none(), label="Estacion", required=False)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fecha inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fecha fin", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    variables = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)
    PROFUNDIDADES = [
        (None, '---------'),
        ('30', '0.3 m'),
        ('50', '0.5 m'),
        ('500', '5 m'),
        ('700', '7 m'),
        ('1000', '10 m'),
               ]
    profundidad = forms.ChoiceField(choices=PROFUNDIDADES)

    def __init__(self, *args, **kwargs):
        super(Grafico1Form, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(
            pk__in=Cruce.objects.filter(var_id__var_id__in = vars_calidad).order_by().values_list('est_id').distinct()
        ).distinct()
        self.fields['estacion'].queryset = estaciones
        self.fields['estacion'].label_from_instance = self.label_from_instance
        estacion1 = estaciones[:1].get()
        self.fields['estacion'].initial = estacion1.est_id

        _var = Variable.objects.filter(pk__in=vars_calidad)
        opciones = [[x.var_id, x.var_codigo] for x in _var]
        self.fields['variables'].choices = opciones

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo



class AsociacionHidroForm(forms.ModelForm):
    class Meta:
        model = models.AsociacionHidro
        fields = "__all__"
        widgets = {
            # "estacion_calidad": s2forms.Select2Widget(),
            "estaciones_hidro": admin.widgets.FilteredSelectMultiple("Estaciones Hidrología", is_stacked=False),
        }

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)

    def __init__(self, *args, **kwargs):
        super(AsociacionHidroForm, self).__init__(*args, **kwargs)
        estacion_calidad = Estacion.objects.filter(tipo__nombre='Calidad de agua').distinct()
        self.fields['estacion_calidad'].queryset = estacion_calidad
        estaciones_hidro = Estacion.objects.exclude(tipo__nombre__in=['Calidad de agua', 'Aforo']).distinct()
        self.fields['estaciones_hidro'].queryset = estaciones_hidro


class CompararHidroForm(forms.Form):
    # frecuencia = forms.ModelChoiceField(queryset=TipoFrecuencia.objects.none(), label="Frecuencia", required=True)
    frecuencia = forms.ModelChoiceField(queryset=TipoFrecuencia.objects.all().order_by('id'), label="Frecuencia", required=True)
    inicio = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fecha inicio", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    fin = forms.DateField(
        input_formats=['%Y-%m-%d'], label="Fecha fin", required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    est_calidad = forms.ModelChoiceField(queryset=Estacion.objects.none(), label="Est. Calidad")
    PROFUNDIDADES = [
        (None, '---------'),
        ('30', '0.3 m'),
        ('50', '0.5 m'),
        ('500', '5 m'),
        ('700', '7 m'),
        ('1000', '10 m'),
               ]
    profundidad = forms.ChoiceField(choices=PROFUNDIDADES)
    var_calidad = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)

    est_hidro = forms.ModelChoiceField(queryset=Estacion.objects.none(), label="Est. Hidro")
    var_hidro = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        if len(kwargs):
            user = kwargs.pop('user')
        elif len(args):
            user = args[1]['user']

        super(CompararHidroForm, self).__init__(*args, **kwargs)
        # if user.username == 'admin':
        #     frecuencia_queryset = TipoFrecuencia.objects.all().order_by('id')
        # else:
        #     try:
        #         uf = UsuarioTipoFrecuencia.objects.filter(usuario=user)
        #         frecuencia_queryset = TipoFrecuencia.objects.filter(pk__in=uf.values('tipofrecuencia_id')).order_by('id')
        #     except:
        #         ## Aquí vendría AnonymousUser
        #         frecuencia_queryset = TipoFrecuencia.objects.filter(pk__in=(2,3,4,5)).order_by('id')
        #
        # self.fields['frecuencia'].queryset = frecuencia_queryset

        # est_calidad = Estacion.objects.filter(
        #     pk__in=Cruce.objects.filter(var_id__var_id__in=vars_calidad).order_by().values_list('est_id').distinct()
        # ).distinct()
        est_calidad = Estacion.objects.filter(tipo__nombre='Calidad de agua').distinct()
        self.fields['est_calidad'].queryset = est_calidad
        self.fields['est_calidad'].label_from_instance = self.label_from_instance
        est_calidad1 = est_calidad[:1].get()
        self.fields['est_calidad'].initial = est_calidad1.est_id

        _var_calidad = Variable.objects.filter(pk__in=vars_calidad)
        opciones_calidad = [[x.var_id, x.var_codigo] for x in _var_calidad]
        self.fields['var_calidad'].choices = opciones_calidad

        asociacion_hidro = models.AsociacionHidro.objects.get(estacion_calidad=est_calidad1)
        est_hidro = Estacion.objects.filter(
            pk__in=asociacion_hidro.estaciones_hidro.values_list('est_id',flat=True)
        ).distinct()
        self.fields['est_hidro'].queryset = est_hidro
        self.fields['est_hidro'].label_from_instance = self.label_from_instance
        est_hidro1 = est_hidro[:1].get()
        self.fields['est_hidro'].initial = est_hidro1.est_id

        _var_hidro = Variable.objects.filter(pk__in=vars_hidro)
        opciones_hidro = [[x.var_id, x.var_nombre] for x in _var_hidro]
        self.fields['var_hidro'].choices = opciones_hidro

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo


class UsuarioVariableForm(forms.ModelForm):
    class Meta:
        model = models.UsuarioVariable
        fields = "__all__"
        widgets = {
            # "usuario": s2forms.Select2Widget(),
            "variable": admin.widgets.FilteredSelectMultiple("Variable", is_stacked=False),
        }

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)

    def __init__(self, *args, **kwargs):
        super(UsuarioVariableForm, self).__init__(*args, **kwargs)
        usuario = User.objects.exclude(username='admin')
        self.fields['usuario'].queryset = usuario
        variable = Variable.objects.filter(pk__gt=100).distinct()
        self.fields['variable'].queryset = variable
