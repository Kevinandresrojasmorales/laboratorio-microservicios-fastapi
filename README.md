Laboratorio de microservicios con FastAPI
¿De qué trata?
En este laboratorio armé una aplicación dividida en tres servicios:
usuarios, productos y pedidos. Cada uno tiene su propia API hecha con
FastAPI y su propia base de datos PostgreSQL.

También configuré Nginx y Kong para que las solicitudes entren por un
solo punto y se dirijan al servicio que corresponde. Docker Compose
permite levantar los componentes del laboratorio sin tener que iniciar
cada uno por separado.
¿Qué hay en el proyecto?
- usuarios/: API para consultar y validar datos de usuarios.
- productos/: API para consultar y validar datos de productos.
- pedidos/: API para consultar y validar datos de pedidos.
- kong/: configuración de las rutas del API Gateway.
- nginx/: configuración del punto de entrada a la aplicación.
- docker-compose.yml: define los servicios, las bases de datos, las
  redes y sus dependencias.
- .env.example: ejemplo de las variables de entorno usadas para las
  bases de datos.
- docs/: informe y diagrama de la arquitectura.
Cada servicio tiene sus propios archivos de aplicación, pruebas y
Dockerfile.
Herramientas utilizadas
- Python y FastAPI
- PostgreSQL
- Docker y Docker Compose
- Kong Gateway
- Nginx
- Pytest para las pruebas
Antes de empezar
Necesitas tener instalado Docker Desktop y comprobar que esté iniciado.
Docker Compose viene incluido en las versiones actuales de Docker
Desktop.
Cómo ejecutar el laboratorio
1. Descarga o clona el repositorio:
   git clone https://github.com/Kevinandresrojasmorales/laboratorio-microservicios-fastapi.git
   cd laboratorio-microservicios-fastapi
2. Crea el archivo .env a partir del ejemplo. En PowerShell puedes
   ejecutar:
   Copy-Item .env.example .env
   El archivo contiene credenciales de demostración para el
   laboratorio. No las uses en una aplicación real ni publiques
   contraseñas personales.
3. Desde la carpeta principal del proyecto, construye e inicia los
   servicios:
   docker compose up --build
   La primera ejecución puede tardar un poco mientras Docker descarga
   las imágenes y construye los servicios.
4. Cuando los contenedores estén iniciados, abre en el navegador:
   - API de usuarios: http://localhost/usuarios
   - Documentación de usuarios: http://localhost/usuarios/docs
   - API de productos: http://localhost/productos
   - Documentación de productos: http://localhost/productos/docs
   - API de pedidos: http://localhost/pedidos
   - Documentación de pedidos: http://localhost/pedidos/docs
   Nginx recibe las solicitudes por el puerto 80 y Kong las dirige
   según la ruta. Si no carga alguna dirección, revisa el estado de los
   contenedores con docker compose ps y los mensajes con
   docker compose logs.
Para detener los servicios, ejecuta desde la carpeta del proyecto:
docker compose down
Si también necesitas borrar los datos guardados en los volúmenes de las
bases de datos, puedes ejecutar docker compose down -v. Ten en cuenta
que esto elimina esos datos.
Rutas disponibles
Cada servicio incluye una ruta de consulta, una ruta para crear un
registro de demostración y una ruta de salud:
  Servicio          Consultar datos    Crear dato de       Estado
                                       demostración        
  Usuarios          GET /usuarios    POST /usuarios    GET /usuarios/health

  Productos         GET /productos   POST /productos   GET /productos/health
  Pedidos           GET /pedidos     POST /pedidos     GET /pedidos/health
Las solicitudes POST validan los datos recibidos y devuelven una
respuesta de ejemplo, pero no guardan usuarios, productos ni pedidos
en la base de datos. Las bases de datos se usan en este laboratorio
para comprobar la conexión de cada servicio y crear una tabla de
demostración.
Ejecutar las pruebas
Cada servicio tiene sus propias pruebas automatizadas. Para ejecutarlas
localmente, entra en la carpeta del servicio, instala las dependencias
indicadas en su requirements.txt y ejecuta pytest.

Por ejemplo, desde la carpeta usuarios:
cd usuarios
pip install -r requirements.txt
pytest
Puedes repetir el mismo procedimiento en productos y pedidos. Para
probar el proyecto completo con Docker, primero levanta los servicios y
revisa sus estados con docker compose ps.
Unas notas sobre el laboratorio

Repositorio
El código del laboratorio está publicado en GitHub:

https://github.com/Kevinandresrojasmorales/laboratorio-microservicios-fastapi/tree/main
