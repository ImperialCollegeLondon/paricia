from variable.models import Variable, Unidad
from estacion.models import Estacion


class Titulos():
    def titulo_grafico(self, variable):
        # returns var_nombre given var_id
        consulta = list(Variable.objects.filter(var_id=variable))
        return consulta[0]

    def titulo_unidad(self, variable):
        # returns uni_sigla given var_id
        var = list(Variable.objects.filter(var_id=variable).values())
        uni = list(Unidad.objects.filter(uni_id=var[0].get('uni_id_id')).values())
        return (uni[0].get('uni_sigla')).encode('utf-8')
