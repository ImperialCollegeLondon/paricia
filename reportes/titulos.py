from variable.models import Variable, Unidad
from estacion.models import Estacion


class Titulos():
    def titulo_grafico(self, variable):
        # returns var_nombre given var_id
        consulta = list(Variable.objects.filter(var_id=variable))

        return consulta[0]

    def titulo_unidad(self, variable):
        var=Variable.objects.get(var_id=variable)
        return var.uni_id.uni_sigla
