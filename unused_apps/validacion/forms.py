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

from django.forms import (
    CheckboxSelectMultiple,
    ChoiceField,
    DateField,
    DateTimeField,
    Form,
    ModelChoiceField,
    ModelForm,
    MultipleChoiceField,
)

from estacion.models import Estacion
from validacion.models import Validacion
from variable.models import Variable


class ValidacionProcess(ModelForm):
    class Meta:
        model = Validacion
        fields = ["var_id", "est_id"]


class ConsultaValidacionForm(Form):
    estacion = ModelChoiceField(
        required=False, queryset=Estacion.objects.order_by("est_id").all()
    )
    variable = ModelChoiceField(
        required=False, queryset=Variable.objects.order_by("var_id").all()
    )

    def filtrar(self, form):
        estacion_ = form.cleaned_data["estacion"]
        variable_ = form.cleaned_data["variable"]

        if estacion_ and variable_:
            lista = Validacion.objects.filter(est_id=estacion_).filter(var_id=variable_)
        elif (estacion_ != None and estacion_ != "") and (
            variable_ == None or variable_ == ""
        ):
            lista = Validacion.objects.filter(est_id=estacion_)
        elif (variable_ != "" and variable_ != None) and (
            estacion_ == None or estacion_ == ""
        ):
            lista = Validacion.objects.filter(var_id=variable_)
        else:
            lista = Validacion.objects.all()
        return lista


class BorrarForm(Form):
    estacion = ModelChoiceField(queryset=Estacion.objects.order_by("est_id").all())
    variable = ModelChoiceField(queryset=Variable.objects.order_by("var_id").all())
    inicio = DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"],
        label="Fecha de Inicio (yyyy-mm-dd HH:MM:SS)",
    )
    fin = DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], label="Fecha de Fin (yyyy-mm-dd HH:MM:SS)"
    )


class CalidadBorrarDatosForm(Form):
    tipo_datos = [
        [0, "CRUDOS"],
        [1, "VALIDADOS (Validados + Horarios + Diarios + Mensuales)"],
    ]
    tipo = MultipleChoiceField(choices=tipo_datos, widget=CheckboxSelectMultiple)
    estacion = ModelChoiceField(queryset=Estacion.objects.order_by("est_id").all())
    var_ids = (101, 102, 103, 104, 105, 106, 107)
    variable = ModelChoiceField(
        queryset=Variable.objects.filter(pk__in=var_ids), label="Variable"
    )
    profundidad = ChoiceField(choices=[])
    inicio = DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"],
        label="Fecha de Inicio (yyyy-mm-dd HH:MM:SS)",
    )
    fin = DateTimeField(
        input_formats=["%Y-%m-%d %H:%M:%S"], label="Fecha de Fin (yyyy-mm-dd HH:MM:SS)"
    )

    def __init__(self, *args, **kwargs):
        super(CalidadBorrarDatosForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(tipo_id=5)
        self.fields["estacion"].queryset = estaciones
        self.fields["estacion"].label_from_instance = self.label_from_instance
        estacion1 = estaciones[:1].get()
        self.fields["estacion"].initial = estacion1.est_id

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo


class ValidacionForm(Form):
    estacion = ModelChoiceField(
        queryset=Estacion.objects.order_by("est_id").all(),
        required=True,
        label="Estación",
    )
    variable = ModelChoiceField(
        queryset=Variable.objects.order_by("var_id").all(), required=True
    )
    inicio = DateField(
        input_formats=["%Y-%m-%d"], label="Inicio (yyyy-mm-dd)", required=True
    )
    fin = DateField(input_formats=["%Y-%m-%d"], label="Fin (yyyy-mm-dd)", required=True)


class ValidacionCalidadForm(Form):
    estacion = ModelChoiceField(
        queryset=Estacion.objects.none(), required=True, label="Estación"
    )
    var_ids = (101, 102, 103, 104, 105, 106, 107)
    variable = ModelChoiceField(
        queryset=Variable.objects.filter(pk__in=var_ids),
        required=True,
        label="Variable",
    )
    profundidad = ChoiceField(choices=((None, ""),), required=True, label="Profundidad")
    inicio = DateField(
        input_formats=["%Y-%m-%d"], required=True, label="Inicio (yyyy-mm-dd)"
    )
    fin = DateField(input_formats=["%Y-%m-%d"], required=True, label="Fin (yyyy-mm-dd)")

    def __init__(self, *args, **kwargs):
        super(ValidacionCalidadForm, self).__init__(*args, **kwargs)
        estaciones = Estacion.objects.filter(tipo_id=5)
        self.fields["estacion"].queryset = estaciones
        self.fields["estacion"].label_from_instance = self.label_from_instance
        estacion1 = estaciones[:1].get()
        self.fields["estacion"].initial = estacion1.est_id

    @staticmethod
    def label_from_instance(obj):
        return obj.est_codigo
