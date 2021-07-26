Sistema de gestión de información hidroclimatológica
====================================================

Instalación
-----------

1) **Actualizar paquetes de servidor/sistema operativo**


   Este sistema fue exitosamente probado en Ubuntu Server 20.04.

2) **Instalar framework DJANGO ver. 3.x**


3) **Instalar base de datos POSTGRESQL ver. 12**



4) **Sincronizar relojes**


   Los relojes del sistema operativo y la base de datos deben estar iguales y en la misma zona horaria. Esto es importante para la carga de datos desde archivos.

5) **Instalar git**

6) **Crear carpeta de proyecto**

   .. code-block:: bash

      mkdir ~/proyecto

7) **Descargar el código fuente**

   Se debe apuntar a la rama **imhea**. Asegurarse también de que se tiene los permisos de acceso ya que Es un repositorio privado.

   .. code-block:: bash

      cd ~/proyecto
      git clone --branch imhea git@github.com:ICHydro/SEDC_FONAG.git


8) **Instalar entorno virtual**

   .. code-block:: bash

      sudo apt-get install virtualenv


         
9) **Instalar paquetes requeridos en el entorno virtual**

   Se sugiere no crear el entorno virtual dentro de la carpeta del repositorio (**SEDC_FONAG**).

   .. code-block:: bash
   
      virtualenv -p python3 venv
      source venv/bin/activate
      (venv) cd paramh2o
      (venv) pip install -r requirements.txt


10) **Modificar configuración de conexión a base de datos**

   LLene los campos con sus datos: **djangomain/settings.py**

   .. code-block:: bash

      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': 'imhea',
              'USER': 'imhea',
              'PASSWORD': 'imhea',
              'HOST': 'localhost',
              'PORT': '5432'
          }
      }


11) **Crear el usuario en la base de datos**

   Este paso es importante hacerlo en este momento de la instalación, aún más si se va a utilizar el script instalador que se describe en el numeral **12)**.
   Se deberá usar el usuario administrativo: 'postgres'
   
   .. code-block:: bash

      sudo -u postgres psql
      
      

   Suponiendo que nombre de usuario es 'imhea'. Este nombre debe coincidir con la configuración en el archivo **djangomain/settings.py**
      
   .. code-block:: sql

      DROP USER imhea;
      DROP ROLE imhea;
      \password imhea;
      \q
      
      
      
   Finalmente salir de la línea de comandos del usuario linux 'postgres':      

   .. code-block:: bash

      exit     

         

12) **Usar script de ayuda para creación inicial**

   El script **crear.sh** crea una base de datos (Si ya existe, la elimina y la vuelve a crear), genera las tablas (proceso de migración) y crea un usuario administrativo para el interfaz web.
   Para ejecutar este script, ubicarse en la raíz del proyecto:

   **IMPORTANTE:** Tómese en cuenta que el script solicitará el ingreso de clave de usuario administrador **postgres**.

   Para ejecutar el script debe haber activado el entorno virtual.

   .. code-block:: bash

      cd SEDC_FONAG
      chmod +x crear.sh
      ./crear.sh


      
      
13) **Programar ejecución de cálculo automático de reportes faltantes**
   Esto script tiene como finalidad procesar el anuario, así como también desencadenar el cálculo de reportes horario, diario, mensual y anual en caso de que se haya generado un problema en el flujo normal de cálculo.
   

   .. code-block:: bash
   
      crontab -e
      
       
         5 0 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/SEDC_FONAG/manage.py runscript generar_horario_loop
         5 1 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/SEDC_FONAG/manage.py runscript generar_diario_loop
         5 2 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/SEDC_FONAG/manage.py runscript generar_mensual_loop
         5 3 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/SEDC_FONAG/manage.py runscript generar_anual_loop
         5 4 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/SEDC_FONAG/manage.py runscript procesar_anuario
 

      sudo service cron restart
      
