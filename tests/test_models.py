from app.models import init_db, create_task, get_all_tasks, clear_tasks
from tests.conftest import TEST_DB


def test_create_task(test_db):
    """
    Test: Crear una tarea debe retornar un ID
    """
    # Inicializar DB (en memoria para tests)
    init_db(test_db)

    # Crear tarea
    task_id = create_task("Test Task", "This is a test task.", db_path=test_db)
    assert task_id is not None, "La creación de la tarea no retornó un ID"

    # Verificar que retorna un ID
    assert isinstance(task_id, int), "El ID retornado no es un entero"


def test_get_all_tasks(test_db):
    """
    Test: Obtener todas las tareas debe retornar la lista correcta
    """
    # Inicializar DB (en memoria para tests)
    init_db(test_db)

    # Crear tareas
    create_task("Task 1", "First task description.", db_path=test_db)
    create_task("Task 2", "Second task description.", db_path=test_db)

    # Obtener todas las tareas
    tasks = get_all_tasks(test_db)

    # Mostrar todas las tereas
    print("Tareas obtenidas:", tasks)

    # Debug verificar la cantidad de items
    assert len(tasks) == 2, f"Se esperaban 2 tareas, pero se obtuvieron {len(tasks)}"

    # Verificar contenido de las tareas
    titles = [task["title"] for task in tasks]
    assert "Task 1" in titles, "La tarea 'Task 1' no está en la lista"
    assert "Task 2" in titles, "La tarea 'Task 2' no está en la lista"
