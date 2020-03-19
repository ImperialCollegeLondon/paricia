# -*- coding: utf-8 -*-

from variable.models import Variable

from anuarios.models import Precipitacion
from anuarios.models import TemperaturaAire
from anuarios.models import HumedadAire
from anuarios.models import HumedadSuelo
from anuarios.models import PresionAtmosferica
from anuarios.models import TemperaturaAgua
from anuarios.models import Caudal
from anuarios.models import NivelAgua


class Anuarios:
    @staticmethod
    def promedio(dict):
        for k,v in dict.items():
            print(k, v)
