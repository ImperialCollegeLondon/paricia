# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from marca.models import Marca
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


# Create your models here.
class LogMedicion(models.Model):
    log_id = models.AutoField("Id", primary_key=True)
    medicion = models.IntegerField("medicion")
    variable = models.ForeignKey(
        Variable,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Variable")
    estacion = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación")
    marca = models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca Datalogger"
    )
    med_fecha = models.DateTimeField("Fecha", auto_now_add=True)
    med_valor = models.DecimalField("Valor", max_digits=14, decimal_places=6, blank=True, null=True)
    med_maximo = models.DecimalField("Máximo", max_digits=14, decimal_places=6, blank=True, null=True)
    med_minimo = models.DecimalField("Mínimo", max_digits=14, decimal_places=6, blank=True, null=True)
    usuario = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Usuario"
    )
    log_fecha = models.DateTimeField("Fecha", auto_now=True)
    log_accion = models.CharField("Acción", max_length=200)
    log_mensaje = models.TextField("Mensaje")

    class Meta:
        ordering = ('log_fecha',)


class LogMedicionSearchForm(forms.Form):
    estacion = forms.ModelChoiceField(required=False,
                                      queryset=Estacion.objects.order_by('est_id').all(), label='Estación')
    variable = forms.ModelChoiceField(required=False,
                                      queryset=Variable.objects.order_by('var_id').all(), label='Variable')
    lista = []

    def filtrar(self, data):
        if isinstance(data, LogMedicionSearchForm):
            variable = data.cleaned_data['variable']
            estacion = data.cleaned_data['estacion']
        else:
            if data.get('var_id') == 'None':
                variable = None
            else:
                variable = Variable.objects.get(var_id=int(data.get('var_id')))
            if data.get('est_id') == 'None':
                estacion = None
            else:
                estacion = Estacion.objects.get(est_id=int(data.get('est_id')))
        if variable and estacion:
            lista = LogMedicion.objects.filter(
                variable=variable
            ).filter(
                estacion_id=estacion
            )
        elif variable is None and estacion:
            lista = LogMedicion.objects.filter(
                estacion_id=estacion
            )
        elif estacion is None and variable:
            lista = LogMedicion.objects.filter(
                variable=variable
            )
        else:
            lista = LogMedicion.objects.all()
        return lista
