def test_get_all_tasks_empty(client):
    """
    Test: GET /api/tasks sin tareas debe retornar lista vacía
    """
    response = client.get("/api/tasks")

    assert response.status_code == 200

    data = response.get_json()
    assert data == []
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_task(client):
    """
    Test: POST /api/tasks debe crear una tarea y retornarla
    """
    new_task = {"title": "Test task", "description": "Testing", "priority": "high"}

    response = client.post("/api/tasks", json=new_task)

    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data
    assert isinstance(data["id"], int)  # ← Verificar que es int
    assert data["id"] > 0
    assert data["title"] == "Test task"
    assert data["description"] == "Testing"
    assert data["priority"] == "high"
    assert data["completed"] == 0


def test_get_task_by_id(client):
    """
    Test: GET /api/tasks/<id> debe retornar una tarea específica
    """
    # Primero crear una tarea
    new_task = {"title": "Task to get", "priority": "medium"}
    response = client.post("/api/tasks", json=new_task)
    task_id = response.get_json()["id"]

    # Ahora obtener la tarea
    response = client.get(f"/api/tasks/{task_id}")

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == task_id
    assert data["title"] == "Task to get"
    assert data["priority"] == "medium"


def test_get_nonexistent_task(client):
    """
    Test: GET /api/tasks/<id> con ID inexistente debe retornar 404
    """
    response = client.get("/api/tasks/999")

    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data


def test_update_task(client):
    """
    Test: PUT /api/tasks/<id> debe actualizar una tarea
    """
    # Crear tarea
    new_task = {"title": "Original title", "priority": "low"}
    response = client.post("/api/tasks", json=new_task)
    task_id = response.get_json()["id"]

    # Actualizar
    updated_data = {"title": "Updated title", "completed": 1, "priority": "high"}
    response = client.put(f"/api/tasks/{task_id}", json=updated_data)

    assert response.status_code == 200

    data = response.get_json()
    assert data["title"] == "Updated title"
    assert data["completed"] == 1
    assert data["priority"] == "high"


def test_update_nonexistent_task(client):
    """
    Test: PUT /api/tasks/<id> con ID inexistente debe retornar 404
    """
    updated_data = {"title": "Updated"}
    response = client.put("/api/tasks/999", json=updated_data)

    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data


def test_delete_task(client):
    """
    Test: DELETE /api/tasks/<id> debe eliminar una tarea
    """
    # Crear tarea
    new_task = {"title": "Task to delete"}
    response = client.post("/api/tasks", json=new_task)
    task_id = response.get_json()["id"]

    # Eliminar
    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204

    # Verificar que ya no existe
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_nonexistent_task(client):
    """
    Test: DELETE /api/tasks/<id> con ID inexistente debe retornar 404
    """
    response = client.delete("/api/tasks/999")

    assert response.status_code == 404

    data = response.get_json()
    assert "error" in data


def test_create_task_without_title(client):
    """
    Test: POST /api/tasks sin title debe retornar 400
    """
    new_task = {"description": "No title"}
    response = client.post("/api/tasks", json=new_task)

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
