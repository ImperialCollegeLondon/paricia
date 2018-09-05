from django import forms
from sensor.models import Sensor, Tipo
from marca.models import Marca


class SensorSearchForm(forms.Form):
    tipo = forms.ModelChoiceField(label="Tipo", required=False,
                                  queryset=Tipo.objects.order_by('id').all())
    mar_id = forms.ModelChoiceField(label="Marca", required=False,
                                    queryset=Marca.objects.order_by('mar_id').all())

    def filtrar(self, form):
        tipo = form.cleaned_data['tipo']
        mar_id = form.cleaned_data['mar_id']
        # filtra los resultados en base al form
        if tipo and mar_id:
            lista = Sensor.objects.filter(
                tipo=tipo
            ).filter(
                mar_id=mar_id
            )
        elif tipo is None and mar_id:
            lista = Sensor.objects.filter(
                mar_id=mar_id
            )
        elif mar_id is None and tipo:
            lista = Sensor.objects.filter(
                tipo=tipo
            )
        else:
            lista = Sensor.objects.all()
        return lista
