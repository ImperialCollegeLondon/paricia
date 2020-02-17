from reportes.typeI import TypeI
from reportes.typeII import TypeII
from reportes.typeIII import TypeIII
from reportes.typeIV import TypeIV
from reportes.typeV import TypeV
from reportes.typeVI import TypeVI


from cruce.models import Cruce

from django.http import HttpResponse
from sedc.settings import BASE_DIR
# librerias para manejar los archivos EXCEL
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl import Workbook
from openpyxl.drawing.image import Image

from openpyxl.chart import (
    LineChart,
    Reference,
)




def reporte_excel_anuario(form):
    estacion = form.cleaned_data['estacion']
    periodo = form.cleaned_data['anio']
    variables = list(Cruce.objects
                     .filter(est_id=form.cleaned_data['estacion'])

                     )

    # ruta de la imagen
    ruta = str(BASE_DIR) + '/media/logo_fonag.jpg'
    img = Image(ruta)

    # Creamos el libro de trabajo
    wb = Workbook()

    # humedadsuelo,presionatmosferica,temperaturaagua,caudal,nivelagua
    typei = [6, 8, 9, 10, 11]
    # precipitacion
    typeii = [1]
    # temperaturaaire
    typeiii = [2]
    # humedadaire
    typeiv = [3]
    # direccion y velocidad
    typev = [4, 5]
    # radiacion
    typevi = [7]

    obj_typei = TypeI()
    obj_typeii = TypeII()
    obj_typeiii = TypeIII()
    obj_typeiv = TypeIV()
    obj_typev = TypeV()
    obj_typevi = TypeVI()
    for item in variables:
        print(item.var_id.var_nombre)
        variable = item.var_id
        if variable.var_id == 1:
            if len(wb.sheetnames) > 1:
                ws_pre = wb.create_sheet(str(variable.var_nombre))
            else:
                ws_pre = wb.active
                ws_pre.title = variable.var_nombre

            obj_typeii.set_encabezado_excel(ws_pre, estacion, periodo)
            obj_typeii.tabla_excel(ws_pre, estacion, periodo)
            obj_typeii.grafico_excel(ws_pre, estacion, periodo)

    # Establecemos el nombre del archivo
    nombre_archivo = str('"') + str(estacion.est_codigo) + str("_") + str(periodo) + str('.xlsx"')
    # Definimos que el tipo de respuesta a devolver es un archivo de microsoft excel
    response = HttpResponse(content_type="application/ms-excel")
    contenido = "attachment; filename={0}".format(nombre_archivo)
    response["Content-Disposition"] = contenido
    wb.save(response)
    return response
