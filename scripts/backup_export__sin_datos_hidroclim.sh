#!/bin/bash

# * Copia los datos existentes en las tablas a archivos JSON
# * Se excluye las mediciones de todas las variables (p.e. Precipitación, temperatura, etc.)
#       a todos los niveles (crudos, validados, horarios, diarios, mensuales, anuales)
# * Ejecución:
#            source ./backup_export__sin_datos_hidroclim.sh

# 1. Ruta del entorno virtual
#source /home/fonag/git_client/venv_imhea/bin/activate
source /home/program/desarrollo/venv_imhea/bin/activate

# 2. Ruta de ejecutable Django
#alias py_manage="python /home/fonag/git_client/imhea/manage.py"
alias py_manage="python /home/program/desarrollo/imhea/manage.py"

#py_manage dumpdata --indent 2 estacion.pais > estacion_pais.json
#py_manage dumpdata --indent 2 estacion.region > estacion_region.json
#py_manage dumpdata --indent 2 estacion.ecosistema > estacion_ecosistema.json
#py_manage dumpdata --indent 2 estacion.socio > estacion_socio.json
#py_manage dumpdata --indent 2 estacion.tipo > estacion_tipo.json
#py_manage dumpdata --indent 2 estacion.sitio > estacion_sitio.json
#py_manage dumpdata --indent 2 estacion.cuenca > estacion_cuenca.json
#py_manage dumpdata --indent 2 estacion.sitiocuenca > estacion_sitiocuenca.json
#py_manage dumpdata --indent 2 estacion.estacion > estacion_estacion.json


py_manage dumpdata anual.var1anual > anual_var1anual.json
py_manage dumpdata anuarios.var10anuarios > anuarios_var10anuarios.json
py_manage dumpdata anuarios.var1anuarios > anuarios_var1anuarios.json
py_manage dumpdata bitacora.bitacora > bitacora_bitacora.json
py_manage dumpdata cruce.cruce > cruce_cruce.json
py_manage dumpdata datalogger.datalogger > datalogger_datalogger.json
py_manage dumpdata datalogger.marca > datalogger_marca.json
py_manage dumpdata diario.var10diario > diario_var10diario.json
py_manage dumpdata diario.var1diario > diario_var1diario.json
py_manage dumpdata estacion.cuenca > estacion_cuenca.json
py_manage dumpdata estacion.ecosistema > estacion_ecosistema.json
py_manage dumpdata estacion.estacion > estacion_estacion.json
py_manage dumpdata estacion.pais > estacion_pais.json
py_manage dumpdata estacion.region > estacion_region.json
py_manage dumpdata estacion.sitio > estacion_sitio.json
py_manage dumpdata estacion.sitiocuenca > estacion_sitiocuenca.json
py_manage dumpdata estacion.socio > estacion_socio.json
py_manage dumpdata estacion.tipo > estacion_tipo.json
py_manage dumpdata formato.asociacion > formato_asociacion.json
py_manage dumpdata formato.clasificacion > formato_clasificacion.json
py_manage dumpdata formato.delimitador > formato_delimitador.json
py_manage dumpdata formato.extension > formato_extension.json
py_manage dumpdata formato.fecha > formato_fecha.json
py_manage dumpdata formato.formato > formato_formato.json
py_manage dumpdata formato.hora > formato_hora.json
py_manage dumpdata frecuencia.frecuencia > frecuencia_frecuencia.json
py_manage dumpdata frecuencia.tipofrecuencia > frecuencia_tipofrecuencia.json
py_manage dumpdata frecuencia.usuariotipofrecuencia > frecuencia_usuariotipofrecuencia.json
py_manage dumpdata horario.var10horario > horario_var10horario.json
py_manage dumpdata horario.var1horario > horario_var1horario.json
py_manage dumpdata importacion.importacion > importacion_importacion.json
py_manage dumpdata importacion.importaciontemp > importacion_importaciontemp.json
py_manage dumpdata instalacion.instalacion > instalacion_instalacion.json
py_manage dumpdata medicion.caudalviaestacion > medicion_caudalviaestacion.json
py_manage dumpdata medicion.curvadescarga > medicion_curvadescarga.json
py_manage dumpdata medicion.nivelfuncion > medicion_nivelfuncion.json
py_manage dumpdata medicion.var10medicion > medicion_var10medicion.json
py_manage dumpdata medicion.var1medicion > medicion_var1medicion.json
py_manage dumpdata mensual.var10mensual > mensual_var10mensual.json
py_manage dumpdata mensual.var1mensual > mensual_var1mensual.json
py_manage dumpdata sensor.marca > sensor_marca.json
py_manage dumpdata sensor.sensor > sensor_sensor.json
py_manage dumpdata sensor.tipo > sensor_tipo.json
py_manage dumpdata telemetria.alarmaemail > telemetria_alarmaemail.json
py_manage dumpdata telemetria.alarmaestado > telemetria_alarmaestado.json
py_manage dumpdata telemetria.alarmatipoestado > telemetria_alarmatipoestado.json
py_manage dumpdata telemetria.configcalidad > telemetria_configcalidad.json
py_manage dumpdata telemetria.configvisualizar > telemetria_configvisualizar.json
py_manage dumpdata telemetria.televariables > telemetria_televariables.json
py_manage dumpdata validacion.agua > validacion_agua.json
py_manage dumpdata validacion.comentariovalidacion > validacion_comentariovalidacion.json
py_manage dumpdata validacion_v2.consulta > validacion_v2_consulta.json
py_manage dumpdata validacion.validacion > validacion_validacion.json
py_manage dumpdata validacion.var10validado > validacion_var10validado.json
py_manage dumpdata validacion.var1validado > validacion_var1validado.json
py_manage dumpdata variable.control > variable_control.json
py_manage dumpdata variable.curvadescarga > variable_curvadescarga.json
py_manage dumpdata variable.unidad > variable_unidad.json
py_manage dumpdata variable.variable > variable_variable.json


exit

anual_var1anual
anuarios_radiacionmaxima
anuarios_radiacionminima
anuarios_var10anuarios
anuarios_var11anuarios
anuarios_var1anuarios
anuarios_var2anuarios
anuarios_var3anuarios
anuarios_var6anuarios
anuarios_var7anuarios
anuarios_var8anuarios
anuarios_var9anuarios
anuarios_viento
auth_group
auth_group_permissions
auth_permission
auth_user
auth_user_groups
auth_user_user_permissions
bitacora_bitacora
calidad_asociacionhidro
calidad_asociacionhidro_estaciones_hidro
calidad_usuariovariable
calidad_usuariovariable_variable
cruce_cruce
datalogger_datalogger
datalogger_marca
diario_var101diario
diario_var102diario
diario_var103diario
diario_var104diario
diario_var105diario
diario_var106diario
diario_var107diario
diario_var108diario
diario_var10diario
diario_var11diario
diario_var12diario
diario_var13diario
diario_var14diario
diario_var15diario
diario_var16diario
diario_var17diario
diario_var18diario
diario_var19diario
diario_var1diario
diario_var20diario
diario_var21diario
diario_var22diario
diario_var23diario
diario_var24diario
diario_var2diario
diario_var3diario
diario_var4diario
diario_var5diario
diario_var6diario
diario_var7diario
diario_var8diario
diario_var9diario
django_admin_log
django_content_type
django_migrations
django_session
estacion_cuenca
estacion_ecosistema
estacion_estacion
estacion_pais
estacion_region
estacion_sitio
estacion_sitiocuenca
estacion_socio
estacion_tipo
formato_asociacion
formato_clasificacion
formato_delimitador
formato_extension
formato_fecha
formato_formato
formato_hora
frecuencia_frecuencia
frecuencia_tipofrecuencia
frecuencia_usuariotipofrecuencia
horario_var101horario
horario_var102horario
horario_var103horario
horario_var104horario
horario_var105horario
horario_var106horario
horario_var107horario
horario_var108horario
horario_var10horario
horario_var11horario
horario_var12horario
horario_var13horario
horario_var14horario
horario_var15horario
horario_var16horario
horario_var17horario
horario_var18horario
horario_var19horario
horario_var1horario
horario_var20horario
horario_var21horario
horario_var22horario
horario_var23horario
horario_var24horario
horario_var2horario
horario_var3horario
horario_var4horario
horario_var5horario
horario_var6horario
horario_var7horario
horario_var8horario
horario_var9horario
importacion_importacion
importacion_importaciontemp
instalacion_instalacion
medicion_caudalviaestacion
medicion_cursordbclima
medicion_cursoremaaphidro
medicion_curvadescarga
medicion_nivelfuncion
medicion_var101medicion
medicion_var102medicion
medicion_var103medicion
medicion_var104medicion
medicion_var105medicion
medicion_var106medicion
medicion_var107medicion
medicion_var108medicion
medicion_var10medicion
medicion_var11medicion
medicion_var12medicion
medicion_var13medicion
medicion_var14medicion
medicion_var15medicion
medicion_var16medicion
medicion_var17medicion
medicion_var18medicion
medicion_var19medicion
medicion_var1medicion
medicion_var20medicion
medicion_var21medicion
medicion_var22medicion
medicion_var23medicion
medicion_var24medicion
medicion_var2medicion
medicion_var3medicion
medicion_var4medicion
medicion_var5medicion
medicion_var6medicion
medicion_var7medicion
medicion_var8medicion
medicion_var9medicion
mensual_var101mensual
mensual_var102mensual
mensual_var103mensual
mensual_var104mensual
mensual_var105mensual
mensual_var106mensual
mensual_var107mensual
mensual_var108mensual
mensual_var10mensual
mensual_var11mensual
mensual_var12mensual
mensual_var13mensual
mensual_var14mensual
mensual_var15mensual
mensual_var16mensual
mensual_var17mensual
mensual_var18mensual
mensual_var19mensual
mensual_var1mensual
mensual_var20mensual
mensual_var21mensual
mensual_var22mensual
mensual_var23mensual
mensual_var24mensual
mensual_var2mensual
mensual_var3mensual
mensual_var4mensual
mensual_var5mensual
mensual_var6mensual
mensual_var7mensual
mensual_var8mensual
mensual_var9mensual
sensor_marca
sensor_sensor
sensor_tipo
telemetria_alarmaemail
telemetria_alarmaestado
telemetria_alarmatipoestado
telemetria_configcalidad
telemetria_configvisualizar
telemetria_televariables
validacion_agua
validacion_comentariovalidacion
validacion_v2_consulta
validacion_validacion
validacion_var101validado
validacion_var102validado
validacion_var103validado
validacion_var104validado
validacion_var105validado
validacion_var106validado
validacion_var107validado
validacion_var108validado
validacion_var10validado
validacion_var11validado
validacion_var12validado
validacion_var13validado
validacion_var14validado
validacion_var15validado
validacion_var16validado
validacion_var17validado
validacion_var18validado
validacion_var19validado
validacion_var1validado
validacion_var20validado
validacion_var21validado
validacion_var22validado
validacion_var23validado
validacion_var24validado
validacion_var2validado
validacion_var3validado
validacion_var4validado
validacion_var5validado
validacion_var6validado
validacion_var7validado
validacion_var8validado
validacion_var9validado
validacion_viento
variable_control
variable_curvadescarga
variable_unidad
variable_variable


python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/variable_unidad.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/variable_variable.json

python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/estacion_tipo.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/estacion_provincia.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/estacion_cuenca.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/estacion_sistema.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/estacion_sistemacuenca.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/estacion_estacion.json

python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/formato_delimitador.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/formato_extension.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/formato_fecha.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/formato_hora.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/formato_formato.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/formato_clasificacion.json

python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/frecuencia_tipofrecuencia.json

python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/telemetria_alarmatipoestado.json

python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/sensor_marca.json
python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/sensor_tipo.json

python manage.py loaddata /home/program/desarrollo/paramh2o/home/data/datalogger_marca.json