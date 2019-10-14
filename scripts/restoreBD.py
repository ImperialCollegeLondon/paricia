
from django.db import connections
import psycopg2

##la base de datos original en este caso db_sedc
oridb = psycopg2.connect(dbname='sedc_dev', host='localhost', user='postgres',password='postgres')
## la base de datos nuevo con los modelos en este caso_sedc_dev
#newdb = psycopg2.connect(dbname='sedc_dev', host='localhost', user='postgres',password='postgres')

cur_ori = oridb.cursor()
cur_tem = oridb.cursor()
#cur_new = newdb.cursor()

print("antes de ejecutar el cursor")
cur_ori.execute("SELECT tablename FROM pg_catalog.pg_tables where schemaname ='public';");
listblori = cur_ori.fetchall()
cur_ori.close()

for i in listblori:
    cur_tem.execute("select count(*) from public."+i[0])
    print(i[0],cur_tem.fetchone()[0])
    #cur_ori.close()

cur_ori.close()
cur_tem.close()
oridb.close()

#cur_new.close()
#newdb.close()
"""" las tablas de django se deben vaciar primero antes de restaurar la copia 
django_content_type_pkey
auth_permission_pkey
django_migrations_pkey

"""