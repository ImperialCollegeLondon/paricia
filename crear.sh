#!/bin/bash

# Crea base de datos, genera migraciones y crea tablas del sistema
# requiere:
#           1) Postgresql v.10 o superior instalado
#           2) Contraseña de usuario 'postgres' de base de datos y usuario 'postgres' de linux
#           3) Usuario de base de datos no administrativo para dueño de datos, con su clave. Esta información debe
#                     estar configurada en : djangomain/settings.py
#           4) Instalar entorno virtual y activarlo
#           5) Instalar previamente requeriments.txt (OK en versión ubuntu 20.04)
#                   para versiones inferiores ej. ubuntu 18.04 comentar las siguiente líneas:
#                                                                              #pkg-resources==0.0.0
#                                                                              #psycopg2==2.8.5
#                                                                              #pypyodbc==1.3.4.3
#                   e instalarlas manualmente psycopg2 y pypyodbc
#
# IMPORTANTE:
# 1. En caso de existir la base de datos, este script la elimina y crea una nueva (vacía)
# 2. Se eliminarán las migraciones anteriores. Se generarán nuevamente migraciones iniciales.

echo " "
echo "IP/hostname del servidor BDD: ('ENTER' Default: localhost)"
read db_host
if [[ ${db_host} == ""  ]]; then
    db_host='localhost'
fi

echo " "
echo "CONTRASEÑA ADMINISTRATIVA (usuario: postgres) DEBE SER USUARIO postgres: "
read -s db_pass
##  IMPORTANTE: debe apuntar a BDD 'postgres' pues es la administrativa
## hostname:port:database:username:password
echo ${db_host}:5432:postgres:postgres:${db_pass} > ~/.pgpass
chmod 600 ~/.pgpass

echo " "
echo "Nombre de usuario de base de datos. Se asociará con la BDD a crear: ('ENTER' Default: testuser)"
read db_user
if [[ ${db_user} == ""  ]]; then
    db_user='testuser'
fi

### Crear usuario
psql -h ${db_host} -U postgres --no-password -c "CREATE USER ${db_user} WITH NOSUPERUSER NOCREATEDB NOCREATEROLE;"

### Cambiando contraseña
echo " "
echo "Ingrese contraseña del usuario ${db_user}"
psql -h ${db_host} -U postgres --no-password -c "\password ${db_user};"


echo " "
echo "Nombre de Base de datos a crear: ('ENTER' Default: testdb)"
read db_name
if [[ ${db_name} == ""  ]]; then
    db_name='testdb'
fi



#### Eliminando conexiones a la db
psql -h ${db_host} -U postgres --no-password -c "SELECT pg_terminate_backend(pg_stat_activity.pid) \
 FROM pg_stat_activity  WHERE datname = '${db_name}'  AND pid <> pg_backend_pid();"

#### Eliminando la db
psql -h ${db_host} -U postgres --no-password -c "drop database ${db_name}"




#### Creando db vacía
psql -h ${db_host} -U postgres --no-password -c "CREATE DATABASE ${db_name}  WITH  OWNER = ${db_user} \
  ENCODING = 'UTF8'  LC_COLLATE = 'es_EC.UTF-8'  LC_CTYPE = 'es_EC.UTF-8'    TABLESPACE = pg_default \
    CONNECTION LIMIT = -1    TEMPLATE template0; "

rm -rf ~/.pgpass

#### Borrando migraciones anteriores DJANGO
echo " "
echo "Borrando migraciones ..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

#### Generando nuevas migraciones
echo ""
echo "Creando migraciones ..."
python manage.py makemigrations

echo " "
echo "Migrando ..."
python manage.py migrate

echo " "
echo "Creando usuario 'admin' ..."
python manage.py createsuperuser --username admin

