from .models import *
from rest_framework import serializers

class PrecipitacionSerial(serializers.ModelSerializer):
    class Meta:
        model = Precipitacion
        fields = ['estacion_id','fecha','valor']