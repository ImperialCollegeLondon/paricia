# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


# Create your models here.
class Marca(models.Model):
    mar_id = models.AutoField("Id", primary_key=True)
    mar_nombre = models.CharField("Marca", max_length=25)

    def __str__(self):
        return str(self.mar_nombre)

    def get_absolute_url(self):
        return reverse('marca:marca_detail', kwargs={'pk': self.pk})
