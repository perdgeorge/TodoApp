import pytest
from src.db.models.todos import Todo
from tests.factories import make_todo_payload
from fastapi.testclient import TestClient


@pytest.mark.anyio
def test_create_todo(client: TestClient):
    payload = make_todo_payload()
    resp = client.post("/todos", json=payload.model_dump())
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload.title
    assert data["description"] == payload.description
    assert "id" in data


@pytest.mark.anyio
def test_get_todo(client: TestClient, todo: Todo):
    resp = client.get(f"/todos/{todo.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == todo.id
    assert data["title"] == todo.title
    assert data["description"] == todo.description


@pytest.mark.anyio
def test_list_todos(client: TestClient, todo_factory: callable):
    t1 = todo_factory()
    t2 = todo_factory()
    resp = client.get("/todos")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    ids = {u["id"] for u in resp.json()}
    assert ids == {t1.id, t2.id}


@pytest.mark.anyio
def test_update_todo(client: TestClient, todo: Todo):
    new_payload = make_todo_payload()
    resp = client.put(f"/todos/{todo.id}", json=new_payload.model_dump())
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == todo.id
    assert data["title"] == todo.title
    assert data["description"] == todo.description
