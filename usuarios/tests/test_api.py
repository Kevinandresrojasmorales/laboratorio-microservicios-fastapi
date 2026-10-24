from fastapi.testclient import TestClient

from app import main


def test_listar():
    with TestClient(main.app) as client:
        response = client.get("/usuarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()


def test_health():
    with TestClient(main.app) as client:
        response = client.get("/usuarios/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    with TestClient(main.app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json()["servicio"] == "usuarios"


def test_crear_dato():
    payload = {"nombre": "Laura"}
    with TestClient(main.app) as client:
        response = client.post("/usuarios", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == 3


def test_rechaza_dato_invalido():
    with TestClient(main.app) as client:
        response = client.post("/usuarios", json={"nombre": "A"})
    assert response.status_code == 422
