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
from django.forms import ModelForm

from estacion.models import Estacion

# from variable.models import Parametro


class AnuarioForm(ModelForm):
    class Meta:
        model = Estacion
        fields = ["est_id"]

    # ESTACION = lista_estaciones()
    YEAR = (
        ("1999", "1999"),
        ("2000", "2000"),
        ("2001", "2001"),
        ("2002", "2002"),
        ("2003", "2003"),
        ("2004", "2004"),
        ("2005", "2005"),
        ("2006", "2006"),
        ("2007", "2007"),
        ("2008", "2008"),
        ("2009", "2009"),
        ("2010", "2010"),
        ("2011", "2011"),
        ("2012", "2012"),
        ("2013", "2013"),
        ("2014", "2014"),
        ("2015", "2015"),
        ("2016", "2016"),
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
    )
    lista = []
    consulta = Estacion.objects.filter(est_externa=False, tipo__in=(1, 2, 3)).order_by(
        "est_codigo"
    )
    estacion = forms.ModelChoiceField(queryset=consulta, empty_label="Estación")
    anio = forms.ChoiceField(choices=YEAR, label="Año")
