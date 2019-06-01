
import psycopg2

##la base de datos original en este caso db_sedc
oridb = psycopg2.connect(dbname='local_db', host='localhost')
## la base de datos nuevo con los modelos en este caso_sedc_dev
newdb = psycopg2.connect(dbname='remote_db', host='some.other.server')

cur_ori= oridb.cursor()
cur_new = newdb.cursor()


listblori = cur_ori.execute("SELECT tablename FROM pg_catalog.pg_tables where schemaname ='public';");

print(listblori);

