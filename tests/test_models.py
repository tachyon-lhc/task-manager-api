from app.models import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)


def test_create_task(test_db):
    """
    Test: Crear una tarea debe retornar un ID
    """
    # Crear tarea
    task_id = create_task("Test Task", "This is a test task.", db_path=test_db)

    # Verificar que retorna un ID válido
    assert task_id is not None, "La creación de la tarea no retornó un ID"
    assert isinstance(task_id, int), "El ID retornado no es un entero"
    assert task_id > 0, "El ID debe ser mayor que 0"


def test_get_all_tasks(test_db):
    """
    Test: Obtener todas las tareas debe retornar la lista correcta
    """
    # Crear tareas
    create_task("Task 1", "First task description.", db_path=test_db)
    create_task("Task 2", "Second task description.", db_path=test_db)

    # Obtener todas las tareas
    tasks = get_all_tasks(test_db)

    # Verificar la cantidad de items
    assert len(tasks) == 2, f"Se esperaban 2 tareas, pero se obtuvieron {len(tasks)}"

    # Verificar contenido de las tareas
    titles = [task["title"] for task in tasks]
    assert "Task 1" in titles, "La tarea 'Task 1' no está en la lista"
    assert "Task 2" in titles, "La tarea 'Task 2' no está en la lista"


def test_get_task_by_id(test_db):
    """
    Test: Obtener una tarea por ID debe retornar la tarea correcta
    """
    # Crear tarea
    task_id = create_task("Get by id", "description by id", db_path=test_db)

    # Obtener tarea por ID
    data = get_task_by_id(task_id, test_db)

    # Verificar datos
    assert data is not None, "No se encontró la tarea"
    assert data["id"] == task_id
    assert data["title"] == "Get by id"
    assert data["description"] == "description by id"


def test_update_task(test_db):
    """
    Test: Actualizar una tarea debe modificar sus campos correctamente
    """
    # Crear tarea
    task_id = create_task(
        "for update", "description for update", "low", db_path=test_db
    )

    # Nuevos valores
    new_title = "already updated"
    new_description = "description updated"
    new_priority = "high"
    new_completed = 1

    # Actualizar
    flag_update = update_task(
        task_id,
        new_title,
        new_description,
        new_completed,
        new_priority,
        db_path=test_db,
    )

    # Verificar que la actualización fue exitosa
    assert flag_update, "update_task retornó False"

    # Obtener tarea actualizada
    data = get_task_by_id(task_id, test_db)

    # Verificar cambios
    assert data["title"] == new_title
    assert data["description"] == new_description
    assert data["priority"] == new_priority
    assert data["completed"] == new_completed


def test_delete_task(test_db):
    """
    Test: Eliminar una tarea debe removerla de la base de datos
    """
    # Crear tarea
    task_id = create_task("Task to delete", db_path=test_db)

    # Verificar que existe
    task = get_task_by_id(task_id, test_db)
    assert task is not None, "La tarea no se creó"

    # Eliminar
    result = delete_task(task_id, test_db)
    assert result, "delete_task retornó False"

    # Verificar que ya no existe
    task = get_task_by_id(task_id, test_db)
    assert task is None, "La tarea no se eliminó"


def test_delete_nonexistent_task(test_db):
    """
    Test: Intentar eliminar una tarea inexistente debe retornar False
    """
    result = delete_task(999, test_db)
    assert result is False, "Debería retornar False para tarea inexistente"
