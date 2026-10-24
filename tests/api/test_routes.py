from fastapi.testclient import TestClient

from app.api.dependencies import get_repository
from app.main import app

client = TestClient(app)


def setup_function():
    get_repository.cache_clear()  # repository bersih untuk tiap test


def test_create_and_get_task():
    r = client.post("/tasks", json={"title": "Belajar"})
    assert r.status_code == 201
    assert client.get(f"/tasks/{r.json()['id']}").json()["title"] == "Belajar"


def test_empty_title_returns_400():
    assert client.post("/tasks", json={"title": " "}).status_code == 400


def test_not_found_returns_404():
    assert client.get("/tasks/999").status_code == 404


def test_update_done_task_returns_409():
    tid = client.post("/tasks", json={"title": "T"}).json()["id"]
    client.post(f"/tasks/{tid}/complete")
    assert client.patch(f"/tasks/{tid}", json={"title": "X"}).status_code == 409
