
import pytest
from app import app, tasks


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    yield
    tasks.clear()


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_create_task():
    client = app.test_client()
    response = client.post(
        "/tasks",
        json={"title": "Learn DevSecOps"}
    )
    assert response.status_code == 201
    assert response.json["title"] == "Learn DevSecOps"


def test_reject_empty_title():
    client = app.test_client()
    response = client.post("/tasks", json={"title": " "})
    assert response.status_code == 400


def test_get_tasks():
    client = app.test_client()
    client.post("/tasks", json={"title": "Test task"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 1
