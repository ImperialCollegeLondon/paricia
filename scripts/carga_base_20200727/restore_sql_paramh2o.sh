#!/bin/bash

# RESTORE tablas individualmente. Solo datos (no esquema)
# Script lee tablas en el directorio de ejecucion


db_nombre='testparamh2o'
#db_user='user1'
db_user='postgres'
db_host='localhost'

echo "Ingrese contraseña de usuario ${db_user}:"
read db_pass
echo ${db_host}:5432:${db_nombre}:${db_user}:${db_pass} > ~/.pgpass
chmod 600 ~/.pgpass


# ###################################################################
## Nota: deben estar en un orden específico para que no haga conflicto por pk inexistentes
tablas=(
#  new_auth_user
#  new_auth_user_user_permissions

  estacion_provincia
  estacion_tipo
  estacion_sitio
  estacion_cuenca
  estacion_sitiocuenca
  estacion_estacion
  datalogger_marca
  datalogger_datalogger
  sensor_tipo
  sensor_marca
  sensor_sensor
  variable_unidad
  variable_variable
  variable_control
  variable_curvadescarga
  frecuencia_frecuencia

#  new_frecuencia_tipofrecuencia
#  new_frecuencia_usuariotipofrecuencia

  cruce_cruce
  bitacora_bitacora
  formato_delimitador
  formato_extension
  formato_fecha
  formato_hora
  formato_formato
  formato_clasificacion
  formato_asociacion
  importacion_importaciontemp
  importacion_importacion
  instalacion_instalacion
  medicion_caudalviaestacion
  medicion_cursordbclima
  medicion_cursoremaaphidro
  medicion_curvadescarga
  telemetria_alarmaemail
  telemetria_alarmatipoestado
  telemetria_alarmaestado
  telemetria_configvisualizar
  telemetria_televariables
  validacion_comentariovalidacion
  validacion_validacion

medicion_var101medicion
medicion_var102medicion
medicion_var103medicion
medicion_var104medicion
medicion_var105medicion
medicion_var106medicion
medicion_var107medicion
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

validacion_var101validado
validacion_var102validado
validacion_var103validado
validacion_var104validado
validacion_var105validado
validacion_var106validado
validacion_var107validado
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

horario_var101horario
horario_var102horario
horario_var103horario
horario_var104horario
horario_var105horario
horario_var106horario
horario_var107horario
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

diario_var101diario
diario_var102diario
diario_var103diario
diario_var104diario
diario_var105diario
diario_var106diario
diario_var107diario
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

mensual_var101mensual
mensual_var102mensual
mensual_var103mensual
mensual_var104mensual
mensual_var105mensual
mensual_var106mensual
mensual_var107mensual
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


)

for tabla in ${tablas[*]}
  do
    echo ${tabla}
    pg_dump -h ${db_host} -U ${db_user} -w --no-password   -d ${db_nombre} < ${tabla}.sql
    echo "" && echo ""
  done

rm -rf ~/.pgpass
exit 1
