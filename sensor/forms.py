from django import forms
from sensor.models import Sensor
from marca.models import Marca


class SensorSearchForm(forms.Form):
    sen_nombre = forms.CharField(label="Tipo", required=False)
    mar_id = forms.ModelChoiceField(label="Marca", required=False,
                                    queryset=Marca.objects.order_by('mar_id').all())

    def filtrar(self, form):
        sen_nombre = form.cleaned_data['sen_nombre']
        mar_id = form.cleaned_data['mar_id']
        # filtra los resultados en base al form
        if sen_nombre and mar_id:
            lista = Sensor.objects.filter(
                sen_nombre=sen_nombre
            ).filter(
                mar_id=mar_id
            )
        elif sen_nombre == "" and mar_id:
            lista = Sensor.objects.filter(
                mar_id=mar_id
            )
        elif mar_id is None and sen_nombre:
            lista = Sensor.objects.filter(
                sen_nombre=sen_nombre
            )
        else:
            lista = Sensor.objects.all()
        return lista
