from estacion.models import Estacion
from rest_framework import serializers


class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estacion
        #fields = ['est_id', 'est_codigo', 'est_nombre', 'tipo', 'sistemacuenca']
        fields = '__all__'
