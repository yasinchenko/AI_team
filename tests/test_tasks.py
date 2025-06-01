# tests/test_tasks.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/api/v1/tasks/", json={"title": "Test task"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test task"

def test_task_lifecycle():
    response = client.post("/api/v1/tasks/", json={"title": "Lifecycle Task"})
    assert response.status_code == 200
    task_id = response.json()["id"]

    lifecycle = ["assigned", "waiting_approval", "approved", "done"]
    for stage in lifecycle:
        res = client.post(f"/api/v1/tasks/{task_id}/advance")
        assert res.status_code == 200
        assert res.json()["new_state"] == stage