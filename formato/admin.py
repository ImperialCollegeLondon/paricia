# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from formato.models import Fecha, Hora

admin.site.register(Fecha)
admin.site.register(Hora)
