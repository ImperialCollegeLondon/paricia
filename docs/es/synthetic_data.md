# Datos sintéticos

Los datos sintéticos se pueden agregar a la base de datos para fines de evaluación comparativa utilizando uno de los escenarios en "utilidades/evaluación comparativa" o creando uno propio. Para hacerlo:

- Complete la base de datos con algunos datos iniciales para la `Station`, la `Variable` y todos los modelos requeridos (consulte la sección *Introducción*).
- Instalar las dependencias de desarrollo (lea la sección *Pruebas*)
- Ejecute el escenario de datos sintéticos que desee.

Si ejecuta uno de los integrados, debería ver una barra de progreso para el proceso y, si inicia sesión en el administrador de Django de Paricia (`http://localhost:8000/admin`), verá los registros. para el modelo `Medidas` creciente.
