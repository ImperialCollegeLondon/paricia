#  python manage.py runscript scripts.mantenimiento.actualizar_secuencias_pk

from django.db import connection

sql_seq_key = """
WITH 
col_pk AS (
	SELECT c.column_name AS colname
	FROM information_schema.table_constraints tc 
	JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
	JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
	  AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
	WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = 'variable_variable'
),
seq_name AS (
	SELECT c.relname as seqname 
	FROM pg_class c WHERE c.relkind = 'S' and c.relname LIKE 'variable_variable\_%'
)
SELECT (SELECT colname FROM col_pk),  (SELECT seqname FROM seq_name);
"""

# Por alguna razón se debe aumentar +1 y luego de ingresar en siguiente elemento ya se pone coherente la secuencia
sql_update_seq = "SELECT setval('variable_variable_var_id_seq', COALESCE((SELECT MAX(var_id)+1 FROM variable_variable), 1), false);"


def actualizar_secuencias_pk():
    print("Actualizando sequencias")
    print("-----------------------")
    print("                       ")
    for tabla in list_tabla:
        print("%s" % (tabla,))
        _sql_seq_key = sql_seq_key.replace("variable_variable", tabla)

        try:
            with connection.cursor() as cursor:
                cursor.execute(_sql_seq_key)
                resultado = cursor.fetchone()
            col_pk = resultado[0]
            seq_name = resultado[1]
        except:
            if tabla == "auth_user":
                col_pk = "id"
                seq_name = "auth_user_id_seq"
            else:
                print("        Error: No se pudo obtener sequence o column name")
                continue

        if col_pk is None or seq_name is None:
            print("        Error: No se pudo obtener sequence o column name")
            continue

        _update_seq = sql_update_seq.replace("variable_variable_var_id_seq", seq_name)
        _update_seq = _update_seq.replace("var_id", col_pk)
        _update_seq = _update_seq.replace("variable_variable", tabla)

        try:
            with connection.cursor() as cursor:
                cursor.execute(_update_seq)
                resultado = cursor.fetchone()[0]
            if resultado > 0:
                print("    OK: SEQ = %s" % (resultado))
                continue
        except:
            print("    Error: No se actualizó secuencia")


"""
SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE' ORDER BY table_name;
"""

list_tabla = [
    "anual_var1anual",
    "anuarios_radiacionmaxima",
    "anuarios_radiacionminima",
    "anuarios_var10anuarios",
    "anuarios_var11anuarios",
    "anuarios_var1anuarios",
    "anuarios_var2anuarios",
    "anuarios_var3anuarios",
    "anuarios_var6anuarios",
    "anuarios_var7anuarios",
    "anuarios_var8anuarios",
    "anuarios_var9anuarios",
    "anuarios_viento",
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "auth_user",
    "auth_user_groups",
    "auth_user_user_permissions",
    "bitacora_bitacora",
    "calidad_asociacionhidro",
    "calidad_asociacionhidro_estaciones_hidro",
    "calidad_usuariovariable",
    "calidad_usuariovariable_variable",
    "cruce_cruce",
    "datalogger_datalogger",
    "datalogger_marca",
    "diario_var101diario",
    "diario_var102diario",
    "diario_var103diario",
    "diario_var104diario",
    "diario_var105diario",
    "diario_var106diario",
    "diario_var107diario",
    "diario_var108diario",
    "diario_var10diario",
    "diario_var11diario",
    "diario_var12diario",
    "diario_var13diario",
    "diario_var14diario",
    "diario_var15diario",
    "diario_var16diario",
    "diario_var17diario",
    "diario_var18diario",
    "diario_var19diario",
    "diario_var1diario",
    "diario_var20diario",
    "diario_var21diario",
    "diario_var22diario",
    "diario_var23diario",
    "diario_var24diario",
    "diario_var2diario",
    "diario_var3diario",
    "diario_var4diario",
    "diario_var5diario",
    "diario_var6diario",
    "diario_var7diario",
    "diario_var8diario",
    "diario_var9diario",
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session",
    "estacion_cuenca",
    "estacion_ecosistema",
    "estacion_estacion",
    "estacion_pais",
    "estacion_region",
    "estacion_sitio",
    "estacion_sitiocuenca",
    "estacion_socio",
    "estacion_tipo",
    "formato_asociacion",
    "formato_clasificacion",
    "formato_delimitador",
    "formato_extension",
    "formato_fecha",
    "formato_formato",
    "formato_hora",
    "frecuencia_frecuencia",
    "frecuencia_tipofrecuencia",
    "frecuencia_usuariotipofrecuencia",
    "horario_var101horario",
    "horario_var102horario",
    "horario_var103horario",
    "horario_var104horario",
    "horario_var105horario",
    "horario_var106horario",
    "horario_var107horario",
    "horario_var108horario",
    "horario_var10horario",
    "horario_var11horario",
    "horario_var12horario",
    "horario_var13horario",
    "horario_var14horario",
    "horario_var15horario",
    "horario_var16horario",
    "horario_var17horario",
    "horario_var18horario",
    "horario_var19horario",
    "horario_var1horario",
    "horario_var20horario",
    "horario_var21horario",
    "horario_var22horario",
    "horario_var23horario",
    "horario_var24horario",
    "horario_var2horario",
    "horario_var3horario",
    "horario_var4horario",
    "horario_var5horario",
    "horario_var6horario",
    "horario_var7horario",
    "horario_var8horario",
    "horario_var9horario",
    "importacion_importacion",
    "importacion_importaciontemp",
    "instalacion_instalacion",
    "medicion_caudalviaestacion",
    "medicion_cursordbclima",
    "medicion_cursoremaaphidro",
    "medicion_curvadescarga",
    "medicion_nivelfuncion",
    "medicion_var101medicion",
    "medicion_var102medicion",
    "medicion_var103medicion",
    "medicion_var104medicion",
    "medicion_var105medicion",
    "medicion_var106medicion",
    "medicion_var107medicion",
    "medicion_var108medicion",
    "medicion_var10medicion",
    "medicion_var11medicion",
    "medicion_var12medicion",
    "medicion_var13medicion",
    "medicion_var14medicion",
    "medicion_var15medicion",
    "medicion_var16medicion",
    "medicion_var17medicion",
    "medicion_var18medicion",
    "medicion_var19medicion",
    "medicion_var1medicion",
    "medicion_var20medicion",
    "medicion_var21medicion",
    "medicion_var22medicion",
    "medicion_var23medicion",
    "medicion_var24medicion",
    "medicion_var2medicion",
    "medicion_var3medicion",
    "medicion_var4medicion",
    "medicion_var5medicion",
    "medicion_var6medicion",
    "medicion_var7medicion",
    "medicion_var8medicion",
    "medicion_var9medicion",
    "mensual_var101mensual",
    "mensual_var102mensual",
    "mensual_var103mensual",
    "mensual_var104mensual",
    "mensual_var105mensual",
    "mensual_var106mensual",
    "mensual_var107mensual",
    "mensual_var108mensual",
    "mensual_var10mensual",
    "mensual_var11mensual",
    "mensual_var12mensual",
    "mensual_var13mensual",
    "mensual_var14mensual",
    "mensual_var15mensual",
    "mensual_var16mensual",
    "mensual_var17mensual",
    "mensual_var18mensual",
    "mensual_var19mensual",
    "mensual_var1mensual",
    "mensual_var20mensual",
    "mensual_var21mensual",
    "mensual_var22mensual",
    "mensual_var23mensual",
    "mensual_var24mensual",
    "mensual_var2mensual",
    "mensual_var3mensual",
    "mensual_var4mensual",
    "mensual_var5mensual",
    "mensual_var6mensual",
    "mensual_var7mensual",
    "mensual_var8mensual",
    "mensual_var9mensual",
    "sensor_marca",
    "sensor_sensor",
    "sensor_tipo",
    "telemetria_alarmaemail",
    "telemetria_alarmaestado",
    "telemetria_alarmatipoestado",
    "telemetria_configcalidad",
    "telemetria_configvisualizar",
    "telemetria_televariables",
    "validacion_agua",
    "validacion_comentariovalidacion",
    "validacion_v2_consulta",
    "validacion_validacion",
    "validacion_var101validado",
    "validacion_var102validado",
    "validacion_var103validado",
    "validacion_var104validado",
    "validacion_var105validado",
    "validacion_var106validado",
    "validacion_var107validado",
    "validacion_var108validado",
    "validacion_var10validado",
    "validacion_var11validado",
    "validacion_var12validado",
    "validacion_var13validado",
    "validacion_var14validado",
    "validacion_var15validado",
    "validacion_var16validado",
    "validacion_var17validado",
    "validacion_var18validado",
    "validacion_var19validado",
    "validacion_var1validado",
    "validacion_var20validado",
    "validacion_var21validado",
    "validacion_var22validado",
    "validacion_var23validado",
    "validacion_var24validado",
    "validacion_var2validado",
    "validacion_var3validado",
    "validacion_var4validado",
    "validacion_var5validado",
    "validacion_var6validado",
    "validacion_var7validado",
    "validacion_var8validado",
    "validacion_var9validado",
    "validacion_viento",
    "variable_control",
    "variable_curvadescarga",
    "variable_unidad",
    "variable_variable",
]


def run():
    print("Inicio de actualizacion de secuencias...")
    try:
        actualizar_secuencias_pk()
    except Exception as e:
        print(e)
        raise e
