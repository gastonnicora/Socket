# Índice
1. [Introducción](#servidor-socket-con-flask-socket)
2. [Requisitos](#requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Detener los Contenedores](#detener-los-contenedores)
6. [Eventos](#eventos)
7. [Licencia](#licencia)
8. [Contacto](#contacto)

## Servidor Socket con Flask-Socket
Este proyecto implementa un servidor Flask-Socket que maneja la comunicación en tiempo real entre la API y la interfaz web. 
Utiliza Redis como sistema de mensajería para recibir información de la API. 
El servidor se encarga de gestionar eventos en tiempo real como  actualizaciones de estado y transacciones de pujas.


## Requisitos

Este proyecto se ejecuta utilizando Docker y depende de los siguientes servicios:

- **api**: El servidor principal que maneja la lógica de la aplicación.
- **socket**: Para manejar la comunicación en tiempo real (WebSockets).
- **db**: Contenedor de base de datos (por ejemplo, PostgreSQL o MySQL).
- **redis**: Usado para la gestión de tareas asíncronas con Celery y almacenamiento en caché.
- **celery**: Procesamiento de tareas en segundo plano.
- **web**: La interfaz de usuario para interactuar con la aplicación a través de una página web.


## Tecnologías en socket

- **Flask**: Framework web para crear la API.
- **Flask-SocketIO**: Utilizado para la comunicación en tiempo real con la pagina web .
- **Redis**: Para recibir los datos con la API.
- **Docker**: Para guardar en contenedores los servicios.

## Estructura del Proyecto
  ```bash
    /socket
    │
    ├── app/
    │   ├── __init__.py         # Inicialización del servidor Flask y WebSocket.
    │   ├── redis.py            # Manejo de los eventos enviados por medio de Redis desde la API.
    │   └── socketio.py         # Conexión y manejo de eventos de socket
    ├── Dockerfile              # Archivo para construir el contenedor Docker del servidor Socket.
    ├── docker-compose.yml      # Configuración de Docker Compose para levantar los servicios.
    ├── requirements.txt        # Dependencias de Python necesarias para el servidor Socket.
    └── run.py                  # Archivo para ejecutar el servidor Flask-Socket.
  ```

## Instalación y Configuración

1. **Crear docker-compose**:
    Cree un archivo llamado ``docker-compose.yml`` que contenga:
    ```yaml
    version: '3.3'

    services:
      db:
        image: gastonnicora/remates-sql
        expose:
          - "3306"
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_USER: user
          MYSQL_PASSWORD: user
          MYSQL_DATABASE: Remates
        volumes:
          - db_data:/var/lib/mysql
        networks:
          - mynetwork 

      web:
        image: gastonnicora/remates-vue
        ports:
          - "80:80"
        restart: always
        depends_on:
          - api
          - socket
        networks:
          - socket
          - conn 

      api:
        image: gastonnicora/remates-python
        restart: always
        environment:
          DB_HOST: db:3306
          DB_USER: user
          DB_PASS: user
          DB_NAME: Remates
          REDIS_HOST: redis
        depends_on:
          - db
          - redis
        ports:
          - "4000:4000"
        networks:
          - mynetwork 
          - conn 
      
      socket:
        image: gastonnicora/remates-socket
        restart: always
        environment:
          REDIS_HOST: redis
        depends_on:
          - api
          - redis
        expose:
          - "4001"
        ports:
          - "4001:4001"
        networks:
          - mynetwork
          - socket 

      celery:
        image: gastonnicora/remates-celery
        restart: always
        depends_on:
          - redis
          - api
        ports:
          - "5555:5555"
        expose:
          - "5000" 
        networks:
          - mynetwork 

      phpmyadmin:
        image: phpmyadmin
        restart: always
        environment:
          PMA_HOST: db
          PMA_PORT: 3306
        ports:
          - "90:80"
        depends_on:
          - db
        networks:
          - mynetwork 

      redis:
        image: redis:7-alpine
        expose:
          - "6379"
        volumes:
          - redis_data:/data
        networks:
          - mynetwork

    networks:
      mynetwork:
      socket:
        driver: bridge 
      conn:
        driver: bridge 

    volumes:
      db_data:
      redis_data: 

    ```

2. **Construye y levanta los contenedores con Docker Compose**:

    Asegúrate de que Docker y Docker Compose estén instalados en tu máquina.

    Ejecuta el siguiente comando para construir y levantar los contenedores necesarios:

    ```bash
    docker-compose up --build 
    ```

    Este comando levantará los siguientes contenedores:

    - **api**: Contenedor que ejecuta la API RESTful.
    - **db**: Contenedor de la base de datos (MySQL).
    - **redis**: Contenedor para el almacenamiento de tareas de Celery y la comunicación entre la API, el WebSocket y Celery
    - **celery**: Contenedor para ejecutar tareas asíncronas.
    - **socket**: Contenedor para gestionar las conexiones WebSocket en tiempo real.
    - **web**: Contenedor con la interfaz de usuario 

## Detener los Contenedores
Para detener y eliminar los contenedores en ejecución, ejecuta el siguiente comando:

```bash
docker-compose down
```
Si deseas eliminar también los volúmenes, usa la opción ``-v``:

```bash
docker-compose down -v
```

## Eventos
El servidor Flask-Socket utiliza WebSockets para permitir la comunicación en tiempo real con la interfaz web. 

### Eventos Disponibles:
  - Conexión del cliente:

    ```
    Evento: connect
    Descripción: Cuando un cliente (interfaz web) se conecta al servidor Socket
    Respuesta: 
    ```
  - Notificación de puja:

    ```
    Evento: disconnect
    Descripción: Cuando un usuario cierra la pestaña, ventana o cuando se cambia la pagina, se elimina el usuario de las listas de "habitaciones" de Socket si inicio sesión.
    Respuesta: 
    ```
  - Inicio de sesión:

    ```
    Evento: coneccion
    Descripción: Cuando un cliente inicia sesión guarda los datos en las "habitaciones" de Socket 
    Respuesta: 
    ```
  - Cierre de sesión:

    ```
    Evento: borrarUser
    Descripción: Cuando un usuario cierra sesión, se elimina el usuario de las listas de "habitaciones" de Socket
    Respuesta: 
    ```
  - Unirse a habitación:

    ```
    Evento: join
    Descripción: Cuando un usuario solicita unirse a una habitación
    Respuesta: Una lista con todos los conectados a la habitación
    ```
  - Abandonar a habitación:

    ```
    Evento: leave
    Descripción: Cuando un usuario solicita unirse a una habitación
    Respuesta: Envía a todos que se conectaron a la sala una lista con todos los conectados a la habitación
    ```
  - Emitir puja:

    ```
    Evento: bidRoom
    Descripción: Cuando API informa que una puja fue aprobada
    Respuesta: Envía a todos los que se conectaron al articulo, la información pertinente
    ```
  - Finalizar Articulo:

    ```
    Evento: finishRoom
    Descripción: Cuando API informa que un articulo finalizo su remate
    Respuesta: Envía a todos los que se conectaron al articulo, la información pertinente
    ```
  - Comenzar Articulo:

    ```
    Evento: startRoom
    Descripción: Cuando API informa que un articulo comienza su remate
    Respuesta: Envía a todos los que se conectaron al articulo, la información pertinente
    ```
  - Actualizar Usuario:

    ```
    Evento: updateSession
    Descripción: Cuando API informa que un usuario se actualizo
    Respuesta: Envía a todas las sesiones del usuario nueva información del mismo
    ```

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE.md) para más detalles.

## Contacto
Email: gastonmatias.21@gmail.com
Teléfono: 2345453976