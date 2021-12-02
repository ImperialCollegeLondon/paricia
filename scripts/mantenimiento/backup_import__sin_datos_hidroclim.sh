#!/bin/bash

# * Carga los datos de archivos JSON a la base de datos del proyecto
# * Se excluye las mediciones de todas las variables (p.e. Precipitación, temperatura, etc.)
#       a todos los niveles (crudos, validados, horarios, diarios, mensuales, anuales)
# Ejecución:
#            source ./backup_import__sin_datos_hidroclim.sh

# 1. Ruta del entorno virtual
source /home/fonag/git_client/venv_imhea/bin/activate

# 2. Ruta de ejecutable Django
alias py_manage="python /home/fonag/git_client/imhea/manage.py"

# 3. Ruta de archivos JSON a cargar
JSON_DIR="home/data/imhea/"

#py_manage loaddata ${JSON_DIR}/estacion_pais.json
#py_manage loaddata ${JSON_DIR}/estacion_region.json
#py_manage loaddata ${JSON_DIR}/estacion_ecosistema.json
#py_manage loaddata ${JSON_DIR}/estacion_socio.json
#py_manage loaddata ${JSON_DIR}/estacion_tipo.json
#py_manage loaddata ${JSON_DIR}/estacion_sitio.json
#py_manage loaddata ${JSON_DIR}/estacion_cuenca.json
#py_manage loaddata ${JSON_DIR}/estacion_sitiocuenca.json
#py_manage loaddata ${JSON_DIR}/estacion_estacion.json


py_manage loaddata ${JSON_DIR}/bitacora_bitacora.json
py_manage loaddata ${JSON_DIR}/cruce_cruce.json
py_manage loaddata ${JSON_DIR}/datalogger_datalogger.json
py_manage loaddata ${JSON_DIR}/datalogger_marca.json
py_manage loaddata ${JSON_DIR}/estacion_cuenca.json
py_manage loaddata ${JSON_DIR}/estacion_ecosistema.json
py_manage loaddata ${JSON_DIR}/estacion_estacion.json
py_manage loaddata ${JSON_DIR}/estacion_pais.json
py_manage loaddata ${JSON_DIR}/estacion_region.json
py_manage loaddata ${JSON_DIR}/estacion_sitio.json
py_manage loaddata ${JSON_DIR}/estacion_sitiocuenca.json
py_manage loaddata ${JSON_DIR}/estacion_socio.json
py_manage loaddata ${JSON_DIR}/estacion_tipo.json
py_manage loaddata ${JSON_DIR}/formato_asociacion.json
py_manage loaddata ${JSON_DIR}/formato_clasificacion.json
py_manage loaddata ${JSON_DIR}/formato_delimitador.json
py_manage loaddata ${JSON_DIR}/formato_extension.json
py_manage loaddata ${JSON_DIR}/formato_fecha.json
py_manage loaddata ${JSON_DIR}/formato_formato.json
py_manage loaddata ${JSON_DIR}/formato_hora.json
py_manage loaddata ${JSON_DIR}/frecuencia_frecuencia.json
py_manage loaddata ${JSON_DIR}/frecuencia_tipofrecuencia.json
py_manage loaddata ${JSON_DIR}/frecuencia_usuariotipofrecuencia.json
py_manage loaddata ${JSON_DIR}/importacion_importacion.json
py_manage loaddata ${JSON_DIR}/importacion_importaciontemp.json
py_manage loaddata ${JSON_DIR}/instalacion_instalacion.json
py_manage loaddata ${JSON_DIR}/medicion_caudalviaestacion.json
py_manage loaddata ${JSON_DIR}/medicion_curvadescarga.json
py_manage loaddata ${JSON_DIR}/medicion_nivelfuncion.json
py_manage loaddata ${JSON_DIR}/sensor_marca.json
py_manage loaddata ${JSON_DIR}/sensor_sensor.json
py_manage loaddata ${JSON_DIR}/sensor_tipo.json
py_manage loaddata ${JSON_DIR}/telemetria_alarmaemail.json
py_manage loaddata ${JSON_DIR}/telemetria_alarmaestado.json
py_manage loaddata ${JSON_DIR}/telemetria_alarmatipoestado.json
py_manage loaddata ${JSON_DIR}/telemetria_configcalidad.json
py_manage loaddata ${JSON_DIR}/telemetria_configvisualizar.json
py_manage loaddata ${JSON_DIR}/telemetria_televariables.json
py_manage loaddata ${JSON_DIR}/variable_control.json
py_manage loaddata ${JSON_DIR}/variable_curvadescarga.json
py_manage loaddata ${JSON_DIR}/variable_unidad.json
py_manage loaddata ${JSON_DIR}/variable_variable.json

exit
py_manage loaddata ${JSON_DIR}/medicion_var10medicion.json
py_manage loaddata ${JSON_DIR}/medicion_var1medicion.json
py_manage loaddata ${JSON_DIR}/validacion_var10validado.json
py_manage loaddata ${JSON_DIR}/validacion_var1validado.json
py_manage loaddata ${JSON_DIR}/horario_var10horario.json
py_manage loaddata ${JSON_DIR}/horario_var1horario.json
py_manage loaddata ${JSON_DIR}/diario_var10diario.json
py_manage loaddata ${JSON_DIR}/diario_var1diario.json
py_manage loaddata ${JSON_DIR}/mensual_var10mensual.json
py_manage loaddata ${JSON_DIR}/mensual_var1mensual.json
py_manage loaddata ${JSON_DIR}/anual_var1anual.json
py_manage loaddata ${JSON_DIR}/anuarios_var10anuarios.json
py_manage loaddata ${JSON_DIR}/anuarios_var1anuarios.json
py_manage loaddata ${JSON_DIR}/validacion_agua.json
py_manage loaddata ${JSON_DIR}/validacion_comentariovalidacion.json
py_manage loaddata ${JSON_DIR}/validacion_v2_consulta.json
py_manage loaddata ${JSON_DIR}/validacion_validacion.json