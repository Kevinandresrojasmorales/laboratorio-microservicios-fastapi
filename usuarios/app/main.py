import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Prepara una tabla de demostración en la base de datos del servicio."""
    with engine.begin() as connection:
        connection.execute(
            text(
                """CREATE TABLE IF NOT EXISTS laboratorio_registro (
                    id SERIAL PRIMARY KEY,
                    descripcion VARCHAR(120) NOT NULL
                )"""
            )
        )
    yield


app = FastAPI(
    title="Servicio de Usuarios",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/usuarios/docs",
    openapi_url="/usuarios/openapi.json",
)


class UsuarioEntrada(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)


@app.get("/usuarios/health")
def health():
    """Comprueba la conectividad con la base de datos propia."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "servicio": "usuarios"}


@app.get("/usuarios")
def listar_usuarios():
    """Devuelve datos de ejemplo para demostrar el enrutamiento."""
    return [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Carlos"}]


@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioEntrada):
    """Valida y devuelve un usuario de demostración; no persiste registros."""
    return {"id": 3, "nombre": usuario.nombre}


@app.get("/")
def root():
    return {"servicio": "usuarios", "documentacion": "/usuarios/docs"}
