import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.BOOKS.clear()
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_list_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_book(client):
    response = client.post("/books", json={"title": "Dune", "author": "Frank Herbert"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] == 1
    assert body["title"] == "Dune"


def test_add_book_requires_title(client):
    response = client.post("/books", json={"author": "Nobody"})
    assert response.status_code == 400


def test_get_book_not_found(client):
    response = client.get("/books/99")
    assert response.status_code == 404
