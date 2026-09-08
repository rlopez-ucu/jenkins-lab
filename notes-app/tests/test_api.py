"""API tests through the Flask test client."""

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.store.clear()
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_create_and_list(client):
    created = client.post("/notes", json={"title": "Hola", "body": "mundo"})
    assert created.status_code == 201
    assert created.get_json()["id"] == 1

    listed = client.get("/notes")
    assert listed.status_code == 200
    assert listed.get_json() == [{"id": 1, "title": "Hola", "body": "mundo"}]


def test_create_requires_title(client):
    response = client.post("/notes", json={"body": "sin titulo"})
    assert response.status_code == 400
    assert "title" in response.get_json()["error"]


def test_create_with_invalid_json_is_400(client):
    response = client.post("/notes", data="not json", content_type="application/json")
    assert response.status_code == 400


def test_get_note(client):
    client.post("/notes", json={"title": "Una"})
    assert client.get("/notes/1").status_code == 200
    assert client.get("/notes/2").status_code == 404


def test_delete_note(client):
    client.post("/notes", json={"title": "Borrar"})
    assert client.delete("/notes/1").status_code == 204
    assert client.get("/notes/1").status_code == 404
    assert client.delete("/notes/1").status_code == 404


def test_search_query_param(client):
    client.post("/notes", json={"title": "Jenkins", "body": "pipeline"})
    client.post("/notes", json={"title": "Docker", "body": "imagen"})
    result = client.get("/notes?q=pipe").get_json()
    assert [n["title"] for n in result] == ["Jenkins"]
