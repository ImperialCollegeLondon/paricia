# -*- coding: utf-8 -*-
from django.forms import ModelForm
from validacion.models import Validacion


class ValidacionProcess(ModelForm):
    class Meta:
        model = Validacion
        fields = ['var_id', 'est_id']
