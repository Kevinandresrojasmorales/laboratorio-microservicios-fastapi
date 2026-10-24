# Informe técnico de entrega — Laboratorio de microservicios

## Objetivo
Implementar una arquitectura distribuida demostrativa con tres APIs independientes construidas con FastAPI, un API Gateway Kong, un punto de entrada Nginx y una base de datos PostgreSQL por servicio.

## Componentes
- **Nginx:** único puerto publicado al anfitrión; recibe HTTP en el puerto 80 y reenvía a Kong.
- **Kong Gateway OSS:** enruta las solicitudes según el prefijo `/usuarios`, `/productos` y `/pedidos`, con configuración declarativa y modo DB-less.
- **Microservicios FastAPI:** cada uno expone endpoint de consulta, healthcheck, validación POST y documentación OpenAPI interna.
- **PostgreSQL:** una instancia y un volumen independiente por microservicio.
- **Docker Compose:** orquesta los contenedores y sus dependencias.
- **Calidad:** pytest/coverage, Ruff, Bandit y Locust.

## Decisiones de diseño y seguridad
1. Se separan los datos por servicio y cada base de datos tiene su propio volumen.
2. Las bases de datos no publican puertos al anfitrión.
3. Los servicios se conectan por una red privada Docker declarada `internal: true`. Nginx participa en las redes pública y privada para actuar como única entrada.


