# Administrador de Paricia

Los administradores de Paricia (o superusuarios) tienen plenos poderes para controlar cualquier aspecto de Paricia, desde otorgar permisos a otros usuarios hasta cambiar la visibilidad de los objetos. La excepción a esto es eliminar objetos que tienen dependientes, como se explica en la sección [permisos](./permissions.md).

Hay dos formas de convertirse en un usuario administrador

1. Pedirle a otro administrador que le dé permisos de superusuario a ese usuario. Esto se hace a través del administrador de Paricia. Dentro de la aplicación `Usuarios`, seleccione el usuario cuyos permisos necesitan cambiarse y marque la casilla que le otorga al usuario `Estado de superusuario`, como se muestra en esta imagen:

![Marcar la tercera casilla le otorga al usuario todos los permisos de Paricia](../assets/images/superuser.png)

2. A través de la línea de comandos. Este es un método más avanzado y, por lo general, solo se requiere cuando se configura Paricia por primera vez, ya sea localmente para el desarrollo o en un servidor nuevo. Supondremos que Paricia se ha lanzado usando `docker compose`, como se indica en las [instrucciones de instalación](./installation.md#docker-deployment). Los pasos en este caso son:

1. Abra una terminal y acceda al servidor, si no es para desarrollo local, mediante SSH u otro método.
2. Busque el nombre del contenedor que ejecuta la imagen `paricia` ejecutando `docker ps`. Debería ser algo como `paricia-web-1` o `paricia-app-1`.
3. Cree el superusuario con `docker exec -it paricia-web-1 python manage.py createsuperuser`.
4. Se le solicitará un nombre de usuario, correo electrónico y contraseña. Complete todos los detalles.

Una vez hecho esto, debería poder iniciar sesión en Paricia a través de la interfaz web y acceder al administrador de Paricia.