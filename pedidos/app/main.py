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
    title="Servicio de Pedidos",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/pedidos/docs",
    openapi_url="/pedidos/openapi.json",
)


class PedidoEntrada(BaseModel):
    usuario_id: int = Field(gt=0)
    producto: str = Field(min_length=2, max_length=80)
    cantidad: int = Field(gt=0, le=1000)


@app.get("/pedidos/health")
def health():
    """Comprueba la conectividad con la base de datos propia."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "servicio": "pedidos"}


@app.get("/pedidos")
def listar_pedidos():
    """Devuelve datos de ejemplo para demostrar el enrutamiento."""
    return [
        {"id": 1, "usuario_id": 1, "producto": "Teclado", "cantidad": 1},
        {"id": 2, "usuario_id": 2, "producto": "Mouse", "cantidad": 2},
    ]


@app.post("/pedidos", status_code=201)
def crear_pedido(pedido: PedidoEntrada):
    """Valida y devuelve un pedido de demostración; no persiste registros."""
    return {"id": 3, **pedido.model_dump()}


@app.get("/")
def root():
    return {"servicio": "pedidos", "documentacion": "/pedidos/docs"}
