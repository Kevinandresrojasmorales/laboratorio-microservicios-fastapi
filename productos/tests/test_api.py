from fastapi.testclient import TestClient

from app import main


def test_listar():
    with TestClient(main.app) as client:
        response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()


def test_health():
    with TestClient(main.app) as client:
        response = client.get("/productos/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    with TestClient(main.app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json()["servicio"] == "productos"


def test_crear_dato():
    payload = {"nombre": "Monitor", "precio": 500000}
    with TestClient(main.app) as client:
        response = client.post("/productos", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == 3


def test_rechaza_dato_invalido():
    with TestClient(main.app) as client:
        response = client.post("/productos", json={"nombre": "Monitor", "precio": -1})
    assert response.status_code == 422
