# Laboratorio académico: microservicios con FastAPI, Kong, Nginx y PostgreSQL

Proyecto demostrativo para Programación Web II. Incluye tres APIs independientes (usuarios, productos y pedidos), una base PostgreSQL exclusiva para cada servicio, Kong como API Gateway y Nginx como único punto de entrada publicado.

> **Alcance:** las rutas GET devuelven datos de ejemplo. Las rutas POST validan el cuerpo y devuelven una respuesta demostrativa, pero **no guardan los registros** en PostgreSQL. La tabla `laboratorio_registro` se crea para demostrar conectividad y aislamiento de datos. No es una solución de producción.

## 1. Requisitos
- Docker Desktop instalado y en ejecución (Windows/macOS/Linux) con Docker Compose v2.
- Puerto TCP 80 libre. Si está ocupado, cambia `80:80` en `docker-compose.yml` y usa ese puerto al probar.
- Git y VS Code son recomendados, no obligatorios.

## 2. Estructura
```text
laboratorio_microservicios_fastapi/
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── nginx/nginx.conf
├── kong/kong.yml
├── docs/arquitectura.svg
├── usuarios/{app,tests,Dockerfile,requirements.txt,locustfile.py}
├── productos/{app,tests,Dockerfile,requirements.txt,locustfile.py}
└── pedidos/{app,tests,Dockerfile,requirements.txt,locustfile.py}
```

## 3. Ejecutar en Windows (PowerShell)
1. Extrae el ZIP en una carpeta fácil de encontrar.
2. Abre esa carpeta en VS Code.
3. Abre una terminal PowerShell en la carpeta donde está `docker-compose.yml`.
4. Verifica Docker: `docker --version` y `docker compose version`.
5. (Opcional) copia `.env.example` a `.env` y ajusta las credenciales de demostración. No uses las credenciales de ejemplo en producción.
6. Construye y levanta la arquitectura:

```powershell
docker compose up --build -d
docker compose ps
```

La primera ejecución requiere descargar imágenes y puede tardar. Espera a que los servicios y sus bases estén saludables. Revisa incidencias con `docker compose logs -f`.

## 4. Probar las rutas
En PowerShell usa `curl.exe` para evitar el alias de `curl`:

```powershell
curl.exe -i http://localhost/usuarios
curl.exe -i http://localhost/usuarios/health
curl.exe -i http://localhost/productos
curl.exe -i http://localhost/productos/health
curl.exe -i http://localhost/pedidos
curl.exe -i http://localhost/pedidos/health
curl.exe -i http://localhost/usuarios/docs
```

Las rutas de negocio deben responder HTTP 200 y JSON; las rutas health deben devolver `status: ok`. La documentación OpenAPI de cada servicio se enruta bajo su prefijo: `http://localhost/usuarios/docs`, `http://localhost/productos/docs` y `http://localhost/pedidos/docs`. Así no se necesita publicar los puertos internos de los microservicios.

Crear un usuario de ejemplo (solo valida y responde, no persiste):
```powershell
curl.exe -i -X POST http://localhost/usuarios -H "Content-Type: application/json" -d "{`"nombre`":`"Laura`"}"
```

## 5. Verificar aislamiento de las bases de datos
Ninguna base de datos publica puertos en el equipo anfitrión. En PowerShell:
```powershell
Test-NetConnection localhost -Port 5432
```
Se espera `TcpTestSucceeded: False`, siempre que otro programa no use ese puerto. La red Docker `privada` está marcada como `internal: true`; Nginx conecta ambas redes para recibir tráfico externo y reenviarlo a Kong.

## 6. Pruebas automáticas
Los tests simulan la conexión a la base de datos para que las pruebas unitarias sean repetibles sin levantar PostgreSQL. Desde la raíz del proyecto, ejecuta:

```powershell
docker compose exec usuarios pytest --cov=app --cov-report=term-missing --cov-fail-under=80
docker compose exec productos pytest --cov=app --cov-report=term-missing --cov-fail-under=80
docker compose exec pedidos pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

Calidad estática (por servicio):
```powershell
docker compose exec usuarios ruff check app tests locustfile.py
docker compose exec usuarios ruff format --check app tests locustfile.py
docker compose exec usuarios bandit -r app
```
Repite Ruff y Bandit para `productos` y `pedidos`. Si se necesita generar informes de cobertura separados, ejecuta los comandos de cada servicio y guarda la salida en capturas.

## 7. Prueba de carga con Locust
Desde el contenedor de un servicio, el host de entrada es `http://nginx` porque todos los contenedores están en la red privada compartida:
```powershell
docker compose exec usuarios locust --headless -f locustfile.py -u 100 -r 10 -t 30s --host http://nginx --csv /tmp/locust-usuarios
docker compose cp usuarios:/tmp/locust-usuarios_stats.csv ./locust-usuarios_stats.csv
docker compose cp usuarios:/tmp/locust-usuarios_failures.csv ./locust-usuarios_failures.csv
```
Repite usando `productos` o `pedidos` (ajusta el prefijo del archivo CSV). Evalúa la latencia y los errores. El objetivo de la guía es tiempo de respuesta ≤ 2 segundos con 100 usuarios; **no se afirma que se haya alcanzado hasta ejecutar la prueba y guardar los resultados**.

## 8. Evidencias para la entrega
Crea una carpeta `evidencias/` y guarda capturas o salidas de:
1. `docker compose ps` con todos los servicios activos.
2. Respuestas HTTP 200 de `/usuarios`, `/productos`, `/pedidos` y sus healthchecks.
3. `Test-NetConnection localhost -Port 5432` mostrando que no se expone PostgreSQL.
4. Pytest con cobertura ≥ 80 % por servicio.
5. Ruff sin errores y Bandit con sus hallazgos revisados.
6. CSV/reporte de Locust con 100 usuarios, tasa de fallos y latencias.
7. Diagrama de arquitectura (`docs/arquitectura.svg`).

No incluyas capturas simuladas: ejecuta los comandos en tu equipo y conserva resultados reales.

## 9. Detener y limpiar
```powershell
docker compose down
```
Para borrar también los datos persistidos (acción destructiva):
```powershell
docker compose down -v
```

## 10. Problemas frecuentes
- **Puerto 80 ocupado:** cambia el lado izquierdo de `80:80` por `8080:80`; prueba con `http://localhost:8080`.
- **Un servicio no inicia:** `docker compose logs usuarios`, `docker compose logs productos`, `docker compose logs pedidos` o `docker compose logs kong`.
- **Base de datos no saludable:** espera unos segundos y revisa `docker compose ps`; verifica el nombre de la BD y las credenciales.
- **Kong devuelve 404:** confirma que la ruta incluya el prefijo (`/usuarios`, `/productos`, `/pedidos`) y revisa `kong/kong.yml`.
- **No tienes Docker instalado:** debes instalarlo y abrir Docker Desktop antes de ejecutar el laboratorio.

## 11. Checklist de evaluación
- [ ] Arquitectura completa inicia con `docker compose up --build -d`.
- [ ] Tres microservicios independientes y tres bases de datos separadas.
- [ ] Nginx es el único servicio que publica un puerto.
- [ ] Kong enruta por prefijo.
- [ ] Red privada interna para servicios y bases de datos.
- [ ] Pruebas automatizadas y cobertura ≥ 80 % demostradas.
- [ ] Ruff, Bandit y Locust ejecutados; resultados documentados.
- [ ] Diagrama y evidencias reales preparados.
- [ ] Demostración en vivo preparada.
