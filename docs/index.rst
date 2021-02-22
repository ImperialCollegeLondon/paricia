Sistema de gestión de información hidroclimatológica
====================================================

Instalación
-----------

1) **Actualizar paquetes de servidor/sistema operativo**



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
              'NAME': 'imheatest',
              'USER': 'imhea',
              'PASSWORD': 'imhea',
              'HOST': 'localhost',
              'PORT': '5432'
          }
      }


11) **Usar script de ayuda para creación inicial**

   El script **crear.sh** crea una base de datos (Si ya existe, la elimina y la vuelve a crear), genera las tablas (proceso de migración) y crea un usuario administrativo.
   En caso de usar esta opción ya no deberá ejecutar el paso del numeral **12)** y deberá continuar con el paso **13)**.
   Para ejecutar este script, ubicarse en la raíz del proyecto:

   **IMPORTANTE:** Tómese en cuenta que el script solicitará el ingreso de clave de usuario administrador **postgres**.

   Para ejecutar el script debe haber activado el entorno virtual.

   .. code-block:: bash

      cd SEDC_FONAG
      chmod +x crear.sh
      ./crear.sh


12) **Ejecutar las migraciones Django**

   Use esta opción si no ejecutó el paso del numeral **11)**.

   .. code-block:: bash
   
      (venv) python manage.py makemigrations
      (venv) python manage.py migrate
      

13) **Copiar funciones de la base de datos**

   Estas son las funciones y disparadores (triggers) necesarios para el sistema realice actividades tales como: consultas de datos, insercción de datos por archivo y ejecución automática de cálculos de reportería (generación de horarios, diarios y mensuales).

   .. code-block:: bash
   
      (venv) python manage.py runscript instalar_funciones_postgres
      
      
14) **Programar ejecución de cálculo automático de reportes faltantes**
   Esto script tiene como finalidad desencadenar el cálculo de reportes horario, diario y mensual en caso de que se haya generado un problema en el flujo normal de cálculo.
   

   .. code-block:: bash
   
      crontab -e
      
       
         5 0 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/paramh2o/manage.py runscript generar_horario_loop
         5 1 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/paramh2o/manage.py runscript generar_diario_loop
         5 2 * * * /home/user/proyecto/venv/bin/python /home/user/proyecto/paramh2o/manage.py runscript generar_mensual_loop
 
 

      sudo service cron restart
      
