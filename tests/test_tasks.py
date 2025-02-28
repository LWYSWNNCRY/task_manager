import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def test_task_data():
    """Test data for creating a task."""
    return {"title": "Test task", "description": "Test task description"}


@pytest.fixture
def test_task_update_data():
    """Test data for updating a task."""
    return {"title": "Updated task", "description": "Updated description"}


@pytest.fixture
def created_task(test_task_data):
    """Creates a task for testing."""
    response = client.post("/tasks", json=test_task_data)
    task = response.json()
    yield task
    client.delete(f"/tasks/{task['id']}")


def test_create_task(test_task_data):
    """Creates a task."""
    response = client.post("/tasks", json=test_task_data)
    assert response.status_code == 200
    task = response.json()
    assert "id" in task
    assert task["title"] == test_task_data["title"]
    assert task["description"] == test_task_data["description"]

    client.delete(f"/tasks/{task['id']}")


def test_get_tasks():
    """Retrieves all tasks."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task(created_task):
    """Retrieves a task by ID."""
    task_id = created_task["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == created_task["title"]
    assert task["description"] == created_task["description"]


def test_update_task(test_task_update_data):
    """Updates a task."""
    task_data = {"title": "Old task", "description": "Old description"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json=test_task_update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == test_task_update_data["title"]
    assert updated_task["description"] == test_task_update_data["description"]

    client.delete(f"/tasks/{task_id}")


def test_delete_task():
    """Deletes a task."""
    task_data = {"title": "Task to be deleted", "description": "Description"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Task deleted"}

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
