from django.db import models
from medicion.models import DigVar
# Create your models here.
class Precipitacion(models.Model):
    # estacion = models.ForeignKey( Estacion, on_delete=models.CASCADE)
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    usado_para_anual = models.BooleanField("Usado para anual", default=False)
    max_dia_valor = models.DecimalField("maximo valor en el dia", max_digits=(DigVar.v1.max_dig + 2), decimal_places=DigVar.v1.dec_pla,
                                 null=True)
    max_dia_dia = models.DecimalField("dia del maximo", max_digits=(DigVar.v1.max_dig + 2), decimal_places=DigVar.v1.dec_pla,
                                 null=True)
    min_dia_valor = models.DecimalField("minimo valor en el dia", max_digits=(DigVar.v1.max_dig + 2),
                                        decimal_places=DigVar.v1.dec_pla,
                                        null=True)
    min_dia_dia = models.DecimalField("dia del minimo", max_digits=(DigVar.v1.max_dig + 2),
                                      decimal_places=DigVar.v1.dec_pla,
                                      null=True)
    prom_mes = models.DecimalField("Promedio del mes", max_digits=(DigVar.v1.max_dig + 2),
                                      decimal_places=DigVar.v1.dec_pla,
                                      null=True)
    quan10= models.DecimalField("cuantil 10", max_digits=(DigVar.v1.max_dig + 2),
                                      decimal_places=DigVar.v1.dec_pla,
                                      null=True)

    quan95 = models.DecimalField("cuantil 95", max_digits=(DigVar.v1.max_dig + 2),
                                      decimal_places=DigVar.v1.dec_pla,
                                      null=True)
    dias0 = models.DecimalField("dias sin lluvia", max_digits=(DigVar.v1.max_dig + 2),
                                      decimal_places=DigVar.v1.dec_pla,
                                      null=True)
    dias01 = models.DecimalField("dias lluvias de 0.1", max_digits=(DigVar.v1.max_dig + 2),
                                decimal_places=DigVar.v1.dec_pla,
                                null=True)
    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]



class Caudal(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)
    usado_para_anual = models.BooleanField("Usado para anual", default=False)
    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]